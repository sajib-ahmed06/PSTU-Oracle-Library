import getpass
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
ORACLE_HOME = Path(os.environ.get("ORACLE_HOME", r"C:\oraclexe\app\oracle\product\10.2.0\server"))
SQLPLUS = ORACLE_HOME / "bin" / "sqlplus.exe"
TNS_ADMIN = ROOT / "backend" / "oracle_config"


def oracle_environment(use_local_auth=False):
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

    environment["ORACLE_HOME"] = str(ORACLE_HOME)
    environment["ORACLE_SID"] = "XE"
    environment["NLS_LANG"] = "AMERICAN_AMERICA.WE8MSWIN1252"
    environment["PATH"] = str(ORACLE_HOME / "bin") + os.pathsep + environment.get("PATH", "")

    if use_local_auth:
        environment.pop("TNS_ADMIN", None)
    else:
        environment["TNS_ADMIN"] = str(TNS_ADMIN)

    return environment


def execute(login, script_path, use_local_auth=False, initialization=""):
    command = [str(SQLPLUS), "-L", "/nolog"]
    script = f'SET ECHO OFF\nSET VERIFY OFF\nSET DEFINE OFF\nWHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\nCONNECT {login}\n{initialization}\n@"{script_path}"\nEXIT\n'
    try:
        result = subprocess.run(
            command,
            input=script,
            text=True,
            env=oracle_environment(use_local_auth),
            cwd=ROOT,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        print("Database setup timed out. Check the Oracle service and try again.")
        return False
    except OSError as error:
        print(f"Could not start SQL*Plus: {error}")
        return False
    return result.returncode == 0


def main():
    print("This setup deletes existing library tables and loads sample records.")
    if input("Type RESET to continue: ").strip() != "RESET":
        print("Setup cancelled.")
        return 1
    if not SQLPLUS.exists():
        print(f"Oracle SQL*Plus was not found: {SQLPLUS}")
        return 1

    print("\nPSTU Library Database Setup")
    print("---------------------------")
    from backend.database import settings
    from backend.auth.passwords import hash_password

    config = settings()
    username = config.get("DB_USER", "")
    db_password = config.get("DB_PASSWORD", "")
    dsn = config.get("DB_DSN", "XE")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,29}", username) or not re.fullmatch(r"[A-Za-z0-9_#]{1,30}", db_password):
        print("Set DB_USER and DB_PASSWORD in your private .env first (Oracle identifiers and a password using letters, numbers, _ or #).")
        return 1
    admin_username = input("Choose the initial administrator username: ").strip()
    admin_password = getpass.getpass("Choose the initial administrator password (at least 8 characters): ")
    if not admin_username or len(admin_password) < 8 or any(ord(c) < 32 for c in admin_username):
        print("A username and a password of at least 8 characters are required.")
        return 1
    def bind(name, value):
        escaped = value.replace("'", "''")
        return f"VARIABLE {name} VARCHAR2(4000)\nBEGIN :{name} := '{escaped}'; END;\n/\n"
    bootstrap_values = bind("bootstrap_user", username.upper()) + bind("bootstrap_password", db_password)
    seed_values = bind("seed_admin_username", admin_username) + bind("seed_admin_password", hash_password(admin_password))
    print("Trying Windows SYSDBA authentication...")

    bootstrap = ROOT / "database" / "bootstrap.sql"
    if not execute("/ as sysdba", bootstrap, use_local_auth=True, initialization=bootstrap_values):
        print("\nWindows SYSDBA login is unavailable.")
        password = getpass.getpass("Enter the Oracle SYSTEM password: ")
        if not password or not execute(f"system/{password}@{dsn}", bootstrap, initialization=bootstrap_values):
            print("\nCould not create the configured application schema. Read the Oracle error above.")
            return 1

    print("\nLoading tables and sample data...")
    setup = ROOT / "database" / "setup.sql"
    if not execute(f"{username}/{db_password}@{dsn}", setup, initialization=seed_values):
        print("\nDatabase tables could not be created.")
        return 1

    print("\nDatabase setup completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
