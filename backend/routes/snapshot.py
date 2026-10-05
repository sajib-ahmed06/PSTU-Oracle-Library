"""Snapshot endpoints for the library application."""

from fastapi import APIRouter
from backend.database import rows, collect_reads, read_many
from backend.reservations import reservation_rows
from .books import get_books
from .members import get_students
from .circulation import get_issues
from .fines import get_fines

router = APIRouter()


@router.get("/api/meta")
def get_meta():
    authors = rows(
        "SELECT author_id||'|'||REPLACE(author_name,'|',' ') FROM author ORDER BY author_name",
        ["id", "name"],
        {"id"},
    )
    categories = rows(
        "SELECT category_id||'|'||REPLACE(category_name,'|',' ') FROM category ORDER BY category_name",
        ["id", "name"],
        {"id"},
    )
    return {"authors": authors, "categories": categories}


@router.get("/api/snapshot")
def get_snapshot():
    # Reuse the same query definitions as individual endpoints, with one login.
    with collect_reads() as queries:
        get_books()
        get_students()
        get_issues()
        get_fines()
        get_meta()
        reservation_rows()
    books, students, issues, fines, authors, categories, reservations = read_many(queries)
    return {
        "books": books,
        "students": students,
        "issues": issues,
        "fines": fines,
        "meta": {"authors": authors, "categories": categories},
        "reservations": reservations,
    }
