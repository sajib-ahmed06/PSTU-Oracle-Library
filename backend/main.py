"""Application entry point: authentication, feature routers, and static assets."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.auth import install_authentication, register_auth_routes
from backend.database import ROOT, rows, execute_dml, quote
from backend.validation import form_data, required
from backend.reservations import register_reservations
from backend.reminders.worker import lifespan

from backend.routes.pages import (
    router as pages_router,
    home,
    books_page,
    students_page,
    circulation_page,
    fines_page,
    accounts_page,
    health,
    audit_page,
)

from backend.routes.books import (
    router as books_router,
    get_books,
    add_book,
    get_book_copies,
    reduce_book_stock,
)

from backend.routes.members import (
    router as members_router,
    get_students,
    add_student,
    edit_student,
    update_student_identity,
    toggle_student_membership,
)

from backend.routes.circulation import (
    router as circulation_router,
    get_issues,
    add_issue,
    return_book,
)

from backend.routes.fines import router as fines_router, get_fines, pay_fine, get_fine_payments

from backend.routes.snapshot import router as snapshot_router, get_meta, get_snapshot

from backend.routes.audit import router as audit_router, get_audit

FRONTEND = ROOT / "frontend"

app = FastAPI(
    title="PSTU Library API", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan
)
install_authentication(app)
register_auth_routes(app, FRONTEND, rows, execute_dml, quote, form_data, required)

for router in (
    pages_router,
    books_router,
    members_router,
    circulation_router,
    fines_router,
    snapshot_router,
    audit_router,
):
    app.include_router(router)

register_reservations(app, get_books, get_issues, get_fines)
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
