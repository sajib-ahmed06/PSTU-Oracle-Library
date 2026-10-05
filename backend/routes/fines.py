"""Fines endpoints for the library application."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool
from backend.database import rows, quote, run_sql
from backend.validation import form_data, positive_number, text_field

router = APIRouter()


@router.get("/api/fines/collection-summary")
def get_collection_summary():
    today = datetime.now(timezone(timedelta(hours=6), "Asia/Dhaka")).date()
    day = f"TO_DATE('{today.isoformat()}','YYYY-MM-DD')"
    month = f"TO_DATE('{today.replace(day=1).isoformat()}','YYYY-MM-DD')"
    result = rows(
        "SELECT (SELECT NVL(SUM(paid_amount),0) FROM fine)||'|'||"
        f"(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at>={day} AND paid_at<{day}+1)||'|'||"
        f"(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at>={month} AND paid_at<ADD_MONTHS({month},1)) "
        "FROM dual",
        ["total", "today", "month"],
        {"total", "today", "month"},
    )[0]
    return {**result, "date": today.isoformat(), "month_start": today.replace(day=1).isoformat()}


@router.get("/api/fines")
def get_fines():
    sql = (
        "SELECT f.fine_id||'|'||i.issue_id||'|'||i.student_id||'|'||REPLACE(s.name,'|',' "
        "')||'|'||REPLACE(b.title,'|',' "
        "')||'|'||f.amount||'|'||f.payment_status||'|'||f.paid_amount||'|'||(f.amount-f.paid_amount)"
        " FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id JOIN student s ON "
        "s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id ORDER BY f.fine_id DESC"
    )
    keys = [
        "fine_id",
        "issue_id",
        "student_id",
        "student",
        "title",
        "amount",
        "payment_status",
        "paid_amount",
        "balance",
    ]
    return rows(
        sql, keys, {"fine_id", "issue_id", "student_id", "amount", "paid_amount", "balance"}
    )


@router.post("/api/fines/{fine_id}/pay")
async def pay_fine(fine_id: int, request: Request):
    fine_id = positive_number(fine_id, "fine_id")
    p = await form_data(request)
    if "amount" in p:
        raise HTTPException(
            400, "Custom payment amounts are not allowed; pay the full outstanding fine"
        )
    note = text_field(p["note"], "note", 300) if p.get("note", "").strip() else ""
    await run_in_threadpool(
        run_sql, f"BEGIN\n pay_fine_proc({fine_id}, NULL, {quote(note)});\n COMMIT;\nEND;\n/"
    )
    return {"message": "Fine paid in full"}


@router.get("/api/fines/{fine_id}/payments")
def get_fine_payments(fine_id: int):
    fine_id = positive_number(fine_id, "fine_id")
    return rows(
        (
            f"SELECT payment_id||'|'||amount||'|'||TO_CHAR(paid_at,'YYYY-MM-DD "
            f"HH24:MI:SS')||'|'||REPLACE(actor,'|',' ')||'|'||NVL(REPLACE(note,'|',' '),'~') FROM "
            f"fine_payment WHERE fine_id={fine_id} ORDER BY paid_at DESC,payment_id DESC"
        ),
        ["payment_id", "amount", "paid_at", "actor", "note"],
        {"payment_id", "amount"},
    )
