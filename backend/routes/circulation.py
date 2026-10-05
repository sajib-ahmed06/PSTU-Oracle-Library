"""Circulation endpoints for the library application."""

from fastapi import APIRouter, Request
from starlette.concurrency import run_in_threadpool
from backend.database import rows, run_sql
from backend.validation import form_data, required, positive_number

router = APIRouter()


@router.get("/api/issues")
def get_issues():
    sql = (
        "SELECT i.issue_id||'|'||i.student_id||'|'||i.book_id||'|'||REPLACE(s.name,'|',' "
        "')||'|'||REPLACE(b.title,'|',' "
        "')||'|'||TO_CHAR(i.issue_date,'YYYY-MM-DD')||'|'||NVL(TO_CHAR(i.due_date,'YYYY-MM-DD'),'~')||'|'||NVL(TO_CHAR(i.return_date,'YYYY-MM-DD'),'~')||'|'||i.status||'|'||NVL(TO_CHAR(c.copy_no),'~')||'|'||CASE"
        " WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)"
        " ELSE 0 END||'|'||CASE WHEN i.status='ISSUED' THEN "
        "GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10 ELSE 0 END FROM "
        "issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON "
        "b.book_id=i.book_id LEFT JOIN book_copy c ON c.copy_id=i.copy_id ORDER BY i.issue_date"
        " DESC, i.issue_id DESC"
    )
    keys = [
        "issue_id",
        "student_id",
        "book_id",
        "student",
        "title",
        "issue_date",
        "due_date",
        "return_date",
        "status",
        "copy_no",
        "overdue_days",
        "current_fine",
    ]
    return rows(
        sql, keys, {"issue_id", "student_id", "book_id", "copy_no", "overdue_days", "current_fine"}
    )


@router.post("/api/issues", status_code=201)
async def add_issue(request: Request):
    p = await form_data(request)
    required(p, "studentId", "bookId")
    student_id = positive_number(p["studentId"], "studentId")
    book_id = positive_number(p["bookId"], "bookId")
    selections = [(book_id, p.get("copyId"))]
    for suffix in ("2", "3"):
        if p.get("bookId" + suffix):
            selections.append(
                (positive_number(p["bookId" + suffix], "bookId" + suffix), p.get("copyId" + suffix))
            )
    calls = []
    for selected_book, selected_copy in selections:
        copy_id = positive_number(selected_copy, "copyId") if selected_copy else "NULL"
        calls.append(f"  issue_book_proc({student_id}, {selected_book}, {copy_id});")
    # All selections succeed together, or SQL*Plus rolls the entire batch back.
    sql = "BEGIN\n" + "\n".join(calls) + "\n  COMMIT;\nEND;\n/"
    await run_in_threadpool(run_sql, sql)
    return {"message": f"{len(selections)} book copies issued"}


@router.post("/api/issues/{issue_id}/return")
def return_book(issue_id: int):
    issue_id = positive_number(issue_id, "issue_id")
    run_sql(f"BEGIN\n return_book_proc({issue_id});\n COMMIT;\nEND;\n/")
    return {"message": "Book returned"}
