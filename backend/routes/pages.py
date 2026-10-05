"""Pages endpoints for the library application."""

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse
from backend.auth import current_session, require_admin
from backend.database import ROOT, run_sql

FRONTEND = ROOT / "frontend"


router = APIRouter()


@router.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")


@router.get("/books")
def books_page():
    return FileResponse(FRONTEND / "books.html")


@router.get("/students")
def students_page():
    return FileResponse(FRONTEND / "students.html")


@router.get("/circulation")
def circulation_page():
    return FileResponse(FRONTEND / "circulation.html")


@router.get("/fines")
def fines_page():
    return FileResponse(FRONTEND / "fines.html")


@router.get("/accounts")
def accounts_page(request: Request):
    if current_session(request)["user_type"] != "ADMIN":
        return RedirectResponse("/", status_code=303)
    return FileResponse(FRONTEND / "accounts.html")


@router.get("/api/health")
def health():
    run_sql("SELECT 1 FROM dual;")
    return {"status": "CONNECTED", "database": "Oracle XE 10g"}


@router.get("/audit")
def audit_page(request: Request):
    require_admin(request)
    return FileResponse(FRONTEND / "audit.html")
