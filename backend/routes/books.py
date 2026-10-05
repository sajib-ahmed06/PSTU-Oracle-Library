"""Books endpoints for the library application."""

from fastapi import APIRouter, Request
from starlette.concurrency import run_in_threadpool
from backend.database import rows, quote, run_sql
from backend.validation import form_data, required, positive_number, text_field

router = APIRouter()


@router.get("/api/books")
def get_books(q: str = ""):
    search = quote("%" + q.lower() + "%")
    sql = (
        f"SELECT d.book_id||'|'||REPLACE(d.title,'|',' ')||'|'||REPLACE(d.author_name,'|',' "
        f"')||'|'||REPLACE(d.category_name,'|',' ')||'|'||REPLACE(NVL(d.publisher,'~'),'|',' "
        f"')||'|'||d.quantity||'|'||(d.available_quantity-(SELECT COUNT(*) FROM book_reservation"
        f" r WHERE r.book_id=d.book_id AND r.status='ACTIVE' AND r.expires_at>SYSDATE)) FROM "
        f"book_details d WHERE LOWER(d.title||d.author_name||d.category_name) LIKE {search} "
        f"ORDER BY d.title"
    )
    keys = [
        "book_id",
        "title",
        "author_name",
        "category_name",
        "publisher",
        "quantity",
        "available_quantity",
    ]
    return rows(sql, keys, {"book_id", "quantity", "available_quantity"})


@router.post("/api/books", status_code=201)
async def add_book(request: Request):
    p = await form_data(request)
    required(p, "title", "author", "category", "quantity")
    quantity = positive_number(p["quantity"], "quantity")
    for field, maximum in (("title", 200), ("author", 100), ("category", 100)):
        p[field] = text_field(p[field], field, maximum)
    p["publisher"] = text_field(p.get("publisher") or "PSTU Library", "publisher", 100)
    sql = f"""
DECLARE
  v_author_id author.author_id%TYPE;
  v_category_id category.category_id%TYPE;
  v_book_id book.book_id%TYPE;
BEGIN
  BEGIN
    SELECT author_id INTO v_author_id
    FROM author
    WHERE LOWER(author_name) = LOWER({quote(p['author'])});
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO author(author_name) VALUES({quote(p['author'])})
    RETURNING author_id INTO v_author_id;
  END;

  BEGIN
    SELECT category_id INTO v_category_id
    FROM category
    WHERE LOWER(category_name) = LOWER({quote(p['category'])});
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO category(category_name) VALUES({quote(p['category'])})
    RETURNING category_id INTO v_category_id;
  END;

  BEGIN
    SELECT book_id INTO v_book_id
    FROM book
    WHERE LOWER(TRIM(title)) = LOWER(TRIM({quote(p['title'])}))
      AND author_id = v_author_id
      AND category_id = v_category_id
    FOR UPDATE;

    UPDATE book
    SET quantity = quantity + {quantity},
        available_quantity = available_quantity + {quantity},
        publisher = {quote(p.get('publisher', 'PSTU Library'))}
    WHERE book_id = v_book_id;
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO book(
      title, author_id, category_id, publisher, quantity, available_quantity
    ) VALUES(
      {quote(p['title'])}, v_author_id, v_category_id,
      {quote(p.get('publisher', 'PSTU Library'))}, {quantity}, {quantity}
    );
  END;
  COMMIT;
END;
/"""
    await run_in_threadpool(run_sql, sql)
    return {"message": "Book stock updated"}


@router.get("/api/books/{book_id}/copies")
def get_book_copies(book_id: int):
    book_id = positive_number(book_id, "book_id")
    return rows(
        (
            f"SELECT c.copy_id||'|'||c.copy_no||'|'||CASE WHEN EXISTS (SELECT 1 FROM "
            f"book_reservation r WHERE r.copy_id=c.copy_id AND r.status='ACTIVE' AND "
            f"r.expires_at>SYSDATE) THEN 'RESERVED' ELSE c.status END FROM book_copy c WHERE "
            f"c.book_id={book_id} AND c.status<>'RETIRED' ORDER BY c.copy_no"
        ),
        ["copy_id", "copy_no", "status"],
        {"copy_id", "copy_no"},
    )


@router.post("/api/books/{book_id}/reduce")
async def reduce_book_stock(book_id: int, request: Request):
    book_id = positive_number(book_id, "book_id")
    p = await form_data(request)
    required(p, "quantity")
    quantity = positive_number(p["quantity"], "quantity")
    sql = f"""
DECLARE
  v_available book.available_quantity%TYPE;
BEGIN
  SELECT available_quantity INTO v_available
  FROM book
  WHERE book_id = {book_id}
  FOR UPDATE;

  IF {quantity} > v_available THEN
    RAISE_APPLICATION_ERROR(-20008, 'Only available copies can be removed from stock');
  END IF;

  UPDATE book
  SET quantity = quantity - {quantity},
      available_quantity = available_quantity - {quantity}
  WHERE book_id = {book_id};
  COMMIT;
END;
/"""
    await run_in_threadpool(run_sql, sql)
    return {"message": "Book stock reduced"}
