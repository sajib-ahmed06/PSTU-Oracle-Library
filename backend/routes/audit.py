"""Audit endpoints for the library application."""

import json

from fastapi import APIRouter, HTTPException, Request
from backend.auth import require_admin
from backend.database import rows, quote
from backend.validation import positive_number

router = APIRouter()


@router.get("/api/audit")
def get_audit(request: Request, q: str = "", entity: str = "", action: str = "", page: int = 1):
    require_admin(request)
    page = positive_number(page, "page")
    if len(q) > 100:
        raise HTTPException(400, "Search must contain at most 100 characters")
    entities = {
        "STUDENT",
        "BOOK",
        "AUTHOR",
        "CATEGORY",
        "ISSUE_BOOK",
        "RETURN_BOOK",
        "FINE",
        "LOGIN_USER",
        "ADMIN",
        "BOOK_RESERVATION",
    }
    actions = {"INSERT", "UPDATE", "DELETE", "SNAPSHOT"}
    conditions = ["1=1"]
    if entity:
        if entity not in entities:
            raise HTTPException(400, "Unknown audit entity")
        conditions.append(f"entity = {quote(entity)}")
    if action:
        if action not in actions:
            raise HTTPException(400, "Unknown audit action")
        conditions.append(f"action = {quote(action)}")
    if q.strip():
        # Literal search: identifiers containing % or _ are not wildcards.
        search = quote(q.strip().lower())
        conditions.append(
            f"INSTR(LOWER(actor || entity || TO_CHAR(record_id) || before_data || after_data), {search}) > 0"
        )
    where = " AND ".join(conditions)
    total = rows(f"SELECT COUNT(*) FROM audit_log WHERE {where}", ["total"], {"total"})[0]["total"]
    size = 25
    first, last = (page - 1) * size, page * size
    sql = f"""SELECT audit_id||'|'||TO_CHAR(occurred_at,'YYYY-MM-DD"T"HH24:MI:SS.FF3"Z"')||'|'||
      RAWTOHEX(actor)||'|'||action||'|'||entity||'|'||record_id||'|'||
      NVL(RAWTOHEX(before_data),'~')||'|'||NVL(RAWTOHEX(after_data),'~')
    FROM (
      SELECT ordered_logs.*, ROWNUM AS row_number FROM (
        SELECT * FROM audit_log WHERE {where} ORDER BY audit_id DESC
      ) ordered_logs WHERE ROWNUM <= {last}
    ) WHERE row_number > {first}"""
    items = rows(
        sql,
        ["audit_id", "occurred_at", "actor", "action", "entity", "record_id", "before", "after"],
        {"audit_id", "record_id"},
    )
    for item in items:
        # The installed Oracle 10g client uses WE8MSWIN1252.
        item["actor"] = bytes.fromhex(item["actor"]).decode("cp1252")
        for key in ("before", "after"):
            item[key] = json.loads(bytes.fromhex(item[key]).decode("cp1252")) if item[key] else None
    return {"items": items, "total": total, "page": page, "page_size": size}
