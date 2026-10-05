"""Oracle SQL*Plus transport and row decoding for Oracle XE 10g."""

import logging
import os
import re
import threading
import time
import subprocess
from pathlib import Path
from contextlib import contextmanager
from contextvars import ContextVar

from fastapi import HTTPException
from backend.audit import audit_actor

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
ORACLE_HOME = Path(os.environ.get("ORACLE_HOME", r"C:\oraclexe\app\oracle\product\10.2.0\server"))
SQLPLUS = ORACLE_HOME / "bin" / "sqlplus.exe"
# Oracle XE 10g has few dedicated handlers; page reads must share a small limit.
SQL_SLOTS = threading.BoundedSemaphore(1)
CONNECT_ERRORS = {"ORA-12516", "ORA-12519", "ORA-12520", "ORA-12541", "ORA-12560", "ORA-12170"}
PENDING_READS = ContextVar("pending_reads", default=None)
READ_ERRORS = CONNECT_ERRORS | {"ORA-03113", "ORA-03114", "ORA-01012", "ORA-12535", "ORA-12537"}


def settings():
    result = {}
    env_file = ROOT / ".env"
    if not env_file.exists():
        return dict(os.environ)
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            result[key.strip()] = value.strip()
    result.update(os.environ)
    return result


config = settings()
LOGIN = f"{config.get('DB_USER', '')}/{config.get('DB_PASSWORD', '')}@{config.get('DB_DSN', 'XE')}"


def quote(value):
    text = "" if value is None else str(value)
    if any(ord(character) < 32 for character in text):
        raise HTTPException(400, "Text fields cannot contain control characters")
    return "'" + text.replace("'", "''") + "'"


def run_sql(sql, *, read_batch=False):
    if not SQLPLUS.exists():
        raise HTTPException(500, "Oracle XE SQL*Plus was not found")
    statement = sql.strip().rstrip(";")
    read_only = (
        read_batch
        or bool(re.match(r"^SELECT\b", statement, re.I))
        and ";" not in statement
        and not re.search(r"\bFOR\s+UPDATE\b", statement, re.I)
    )
    actor = audit_actor.get()
    actor_statement = (
        f"BEGIN DBMS_APPLICATION_INFO.SET_CLIENT_INFO({quote(actor)}); END;\n/\n" if actor else ""
    )
    sql = actor_statement + sql
    script = f"SET DEFINE OFF\nSET SQLBLANKLINES ON\nSET HEADING OFF FEEDBACK OFF PAGESIZE 0 LINESIZE 32767 TRIMSPOOL ON TAB OFF VERIFY OFF ECHO OFF\nWHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\n{sql}\nEXIT\n"
    environment = os.environ.copy()
    for key in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "http_proxy",
        "https_proxy",
        "no_proxy",
    ):
        environment.pop(key, None)
    environment["TNS_ADMIN"] = str(ROOT / "backend" / "oracle_config")
    environment["ORACLE_HOME"] = str(ORACLE_HOME)
    environment["PATH"] = str(ORACLE_HOME / "bin") + os.pathsep + environment.get("PATH", "")
    environment["NLS_LANG"] = "AMERICAN_AMERICA.WE8MSWIN1252"
    # Fail before executing SQL when CONNECT is rejected. Only then is retrying a
    # mutation safe; a timeout/disconnect after execution has an unknown outcome.
    connection = (
        "WHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\nCONNECT "
        + LOGIN
        + "\nPROMPT __LIBRARY_CONNECTED__\n"
    )
    for attempt in range(3):
        if not SQL_SLOTS.acquire(timeout=30):
            raise HTTPException(503, "Database is busy. Please try again shortly")
        try:
            result = subprocess.run(
                [str(SQLPLUS), "-S", "-L", "/nolog"],
                input=connection + script,
                text=True,
                capture_output=True,
                env=environment,
                cwd=ROOT,
                timeout=20,
            )
        except OSError as error:
            logging.getLogger(__name__).error("SQL*Plus could not start: %s", error)
            raise HTTPException(503, "Database client could not start")
        except subprocess.TimeoutExpired:
            raise HTTPException(504, "Oracle database did not respond in time")
        finally:
            # Let XE retire its dedicated handler before opening the next one.
            time.sleep(0.15)
            SQL_SLOTS.release()
        output_lines = (result.stdout + result.stderr).splitlines()
        connected = "__LIBRARY_CONNECTED__" in output_lines
        if connected:
            output_lines.remove("__LIBRARY_CONNECTED__")
        output = "\n".join(output_lines).strip()
        errors = [
            line.strip()
            for line in output.splitlines()
            if re.match(r"^(?:ORA|SP2)-\d+:", line.strip())
        ]
        if not result.returncode and not errors:
            return output
        message = errors[0] if errors else "Oracle command failed"
        code = message.split(":", 1)[0]
        if attempt < 2 and (
            (not connected and code in CONNECT_ERRORS) or (read_only and code in READ_ERRORS)
        ):
            logging.getLogger(__name__).warning(
                "Retrying transient Oracle connection error: %s", code
            )
            time.sleep(1 + attempt)
            continue
        break
    if result.returncode or errors:
        if "ORA-00001" in message:
            if "UQ_STUDENT_ROLL" in message:
                raise HTTPException(409, "ID/Roll number is already registered")
            if "UQ_STUDENT_REGISTRATION" in message:
                raise HTTPException(409, "Registration number is already registered")
            raise HTTPException(409, "A record with these details already exists")
        if "ORA-01403" in message:
            raise HTTPException(404, "The requested record was not found")
        if "ORA-200" in message:
            raise HTTPException(409, message.split(":", 1)[-1].strip())
        logging.getLogger(__name__).error("Oracle command failed: %s", message)
        raise HTTPException(503, "Database request failed. Please try again later")
    return output


def rows(sql, keys, numbers=()):
    pending = PENDING_READS.get()
    if pending is not None:
        pending.append((sql, keys, numbers))
        return []
    output = run_sql(sql.rstrip(";") + ";")
    return parse_rows(output, keys, numbers)


def parse_rows(output, keys, numbers=()):
    data = []
    for line in output.splitlines():
        if not line.strip():
            continue
        values = line.strip().split("|")
        if len(values) != len(keys):
            raise HTTPException(502, "The database returned an unexpected row format")
        item = dict(zip(keys, (None if value == "~" else value for value in values)))
        for key in numbers:
            if item.get(key) is not None:
                item[key] = float(item[key]) if "." in str(item[key]) else int(item[key])
        data.append(item)
    return data


def execute_dml(sql):
    statement = sql.rstrip().rstrip(";")
    run_sql(f"{statement};\nCOMMIT;")


@contextmanager
def collect_reads():
    """Collect existing read-query definitions without opening any connection."""
    queries = []
    token = PENDING_READS.set(queries)
    try:
        yield queries
    finally:
        PENDING_READS.reset(token)


def read_many(queries):
    """Execute read-only queries in one SQLPlus connection and decode each section."""
    script = []
    for index, (sql, keys, numbers) in enumerate(queries):
        statement = sql.strip().rstrip(";")
        if (
            not re.match(r"^SELECT\b", statement, re.I)
            or ";" in statement
            or re.search(r"\bFOR\s+UPDATE\b", statement, re.I)
        ):
            raise ValueError("Only read-only SELECT statements can be batched")
        script.extend((f"PROMPT __LIBRARY_READ_{index}__", statement + ";"))
    output = run_sql("\n".join(script), read_batch=True)
    sections = [[] for _ in queries]
    active = None
    for line in output.splitlines():
        marker = re.fullmatch(r"__LIBRARY_READ_(\d+)__", line.strip())
        if marker:
            index = int(marker.group(1))
            if index != (0 if active is None else active + 1) or index >= len(queries):
                raise HTTPException(502, "Unexpected database batch section")
            active = index
        elif active is not None:
            sections[active].append(line)
        elif line.strip():
            raise HTTPException(502, "Unexpected database batch output")
    if queries and active != len(queries) - 1:
        raise HTTPException(502, "Database batch returned incomplete results")
    return [
        parse_rows("\n".join(lines), keys, numbers)
        for lines, (_, keys, numbers) in zip(sections, queries)
    ]
