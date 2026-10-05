# backend/routes/books.py

Read the catalogue and manage physical copies and stock.

Source: [মূল file](../../backend/routes/books.py)। Snapshot 2026-10-04; 136 lines; SHA-256 `a25f291f4780508dcf54968730cdbe3c9f697ffbffa40ba76aff0cd74752b986`।

## Function / object / element inventory

### `get_books` — L12–L31

`def get_books(q: str = ""):`

book_details view থেকে title/author/category search ও available/total stock ফেরায়। Search SQL LIKE হওয়ায় % ও _ wildcard হতে পারে।

### `add_book` — L35–L91

`async def add_book(request: Request):`

Form validate করে author/category resolve বা create করে; matching book row lock করে restock, নয়তো নতুন title insert; transaction শেষে commit।

### `get_book_copies` — L95–L106

`def get_book_copies(book_id: int):`

Test/setup helper: get book copies; নিচের assertions/calls সেই behavior define করে।

### `reduce_book_stock` — L110–L136

`async def reduce_book_stock(book_id: int, request: Request):`

Book lock করে requested quantity available stock ছাড়িয়েছে কি না দেখে; total ও available উভয় count কমায়। Borrowed copies বাদ দেওয়া যায় না।

## সম্পূর্ণ original source

```python
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Books endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import APIRouter, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from backend.database import rows, quote, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.validation import form_data, required, positive_number, text_field</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>@router.get(&quot;/api/books&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 12 | <code>def get_books(q: str = &quot;&quot;):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 13 | <code>    search = quote(&quot;%&quot; + q.lower() + &quot;%&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_books` অংশে |
| 14 | <code>    sql = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_books` অংশে |
| 15 | <code>        f&quot;SELECT d.book_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(d.title,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(d.author_name,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 16 | <code>        f&quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(d.category_name,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(NVL(d.publisher,&#x27;~&#x27;),&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 17 | <code>        f&quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;d.quantity&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;(d.available_quantity-(SELECT COUNT(*) FROM book_reservation&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 18 | <code>        f&quot; r WHERE r.book_id=d.book_id AND r.status=&#x27;ACTIVE&#x27; AND r.expires_at&gt;SYSDATE)) FROM &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_books` অংশে |
| 19 | <code>        f&quot;book_details d WHERE LOWER(d.title&#124;&#124;d.author_name&#124;&#124;d.category_name) LIKE {search} &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 20 | <code>        f&quot;ORDER BY d.title&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 21 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 22 | <code>    keys = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_books` অংশে |
| 23 | <code>        &quot;book_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 24 | <code>        &quot;title&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 25 | <code>        &quot;author_name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 26 | <code>        &quot;category_name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 27 | <code>        &quot;publisher&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 28 | <code>        &quot;quantity&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 29 | <code>        &quot;available_quantity&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 30 | <code>    ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_books` অংশে |
| 31 | <code>    return rows(sql, keys, {&quot;book_id&quot;, &quot;quantity&quot;, &quot;available_quantity&quot;})</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_books` অংশে |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 34 | <code>@router.post(&quot;/api/books&quot;, status_code=201)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 35 | <code>async def add_book(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 36 | <code>    p = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_book` অংশে |
| 37 | <code>    required(p, &quot;title&quot;, &quot;author&quot;, &quot;category&quot;, &quot;quantity&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 38 | <code>    quantity = positive_number(p[&quot;quantity&quot;], &quot;quantity&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 39 | <code>    for field, maximum in ((&quot;title&quot;, 200), (&quot;author&quot;, 100), (&quot;category&quot;, 100)):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `add_book` অংশে |
| 40 | <code>        p[field] = text_field(p[field], field, maximum)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 41 | <code>    p[&quot;publisher&quot;] = text_field(p.get(&quot;publisher&quot;) or &quot;PSTU Library&quot;, &quot;publisher&quot;, 100)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 42 | <code>    sql = f&quot;&quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 43 | <code>DECLARE</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 44 | <code>  v_author_id author.author_id%TYPE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 45 | <code>  v_category_id category.category_id%TYPE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 46 | <code>  v_book_id book.book_id%TYPE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 47 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 48 | <code>  BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 49 | <code>    SELECT author_id INTO v_author_id</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 50 | <code>    FROM author</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 51 | <code>    WHERE LOWER(author_name) = LOWER({quote(p[&#x27;author&#x27;])});</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 52 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 53 | <code>    INSERT INTO author(author_name) VALUES({quote(p[&#x27;author&#x27;])})</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 54 | <code>    RETURNING author_id INTO v_author_id;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 55 | <code>  END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>  BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 58 | <code>    SELECT category_id INTO v_category_id</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 59 | <code>    FROM category</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 60 | <code>    WHERE LOWER(category_name) = LOWER({quote(p[&#x27;category&#x27;])});</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 61 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 62 | <code>    INSERT INTO category(category_name) VALUES({quote(p[&#x27;category&#x27;])})</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 63 | <code>    RETURNING category_id INTO v_category_id;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 64 | <code>  END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>  BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 67 | <code>    SELECT book_id INTO v_book_id</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 68 | <code>    FROM book</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 69 | <code>    WHERE LOWER(TRIM(title)) = LOWER(TRIM({quote(p[&#x27;title&#x27;])}))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 70 | <code>      AND author_id = v_author_id</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 71 | <code>      AND category_id = v_category_id</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 72 | <code>    FOR UPDATE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 73 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 74 | <code>    UPDATE book</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 75 | <code>    SET quantity = quantity + {quantity},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 76 | <code>        available_quantity = available_quantity + {quantity},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 77 | <code>        publisher = {quote(p.get(&#x27;publisher&#x27;, &#x27;PSTU Library&#x27;))}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 78 | <code>    WHERE book_id = v_book_id;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_book` অংশে |
| 79 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 80 | <code>    INSERT INTO book(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 81 | <code>      title, author_id, category_id, publisher, quantity, available_quantity</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 82 | <code>    ) VALUES(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 83 | <code>      {quote(p[&#x27;title&#x27;])}, v_author_id, v_category_id,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 84 | <code>      {quote(p.get(&#x27;publisher&#x27;, &#x27;PSTU Library&#x27;))}, {quantity}, {quantity}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 85 | <code>    );</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 86 | <code>  END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 87 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 88 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 89 | <code>/&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_book` অংশে |
| 90 | <code>    await run_in_threadpool(run_sql, sql)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_book` অংশে |
| 91 | <code>    return {&quot;message&quot;: &quot;Book stock updated&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `add_book` অংশে |
| 92 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 93 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 94 | <code>@router.get(&quot;/api/books/{book_id}/copies&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 95 | <code>def get_book_copies(book_id: int):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 96 | <code>    book_id = positive_number(book_id, &quot;book_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_book_copies` অংশে |
| 97 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_book_copies` অংশে |
| 98 | <code>        (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 99 | <code>            f&quot;SELECT c.copy_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;c.copy_no&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;CASE WHEN EXISTS (SELECT 1 FROM &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 100 | <code>            f&quot;book_reservation r WHERE r.copy_id=c.copy_id AND r.status=&#x27;ACTIVE&#x27; AND &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_book_copies` অংশে |
| 101 | <code>            f&quot;r.expires_at&gt;SYSDATE) THEN &#x27;RESERVED&#x27; ELSE c.status END FROM book_copy c WHERE &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 102 | <code>            f&quot;c.book_id={book_id} AND c.status&lt;&gt;&#x27;RETIRED&#x27; ORDER BY c.copy_no&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_book_copies` অংশে |
| 103 | <code>        ),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 104 | <code>        [&quot;copy_id&quot;, &quot;copy_no&quot;, &quot;status&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 105 | <code>        {&quot;copy_id&quot;, &quot;copy_no&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 106 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_book_copies` অংশে |
| 107 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 108 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 109 | <code>@router.post(&quot;/api/books/{book_id}/reduce&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 110 | <code>async def reduce_book_stock(book_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 111 | <code>    book_id = positive_number(book_id, &quot;book_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 112 | <code>    p = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reduce_book_stock` অংশে |
| 113 | <code>    required(p, &quot;quantity&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 114 | <code>    quantity = positive_number(p[&quot;quantity&quot;], &quot;quantity&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 115 | <code>    sql = f&quot;&quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 116 | <code>DECLARE</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 117 | <code>  v_available book.available_quantity%TYPE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 118 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 119 | <code>  SELECT available_quantity INTO v_available</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 120 | <code>  FROM book</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 121 | <code>  WHERE book_id = {book_id}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 122 | <code>  FOR UPDATE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 123 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 124 | <code>  IF {quantity} &gt; v_available THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 125 | <code>    RAISE_APPLICATION_ERROR(-20008, &#x27;Only available copies can be removed from stock&#x27;);</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 126 | <code>  END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 127 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 128 | <code>  UPDATE book</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 129 | <code>  SET quantity = quantity - {quantity},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 130 | <code>      available_quantity = available_quantity - {quantity}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 131 | <code>  WHERE book_id = {book_id};</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reduce_book_stock` অংশে |
| 132 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 133 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 134 | <code>/&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reduce_book_stock` অংশে |
| 135 | <code>    await run_in_threadpool(run_sql, sql)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reduce_book_stock` অংশে |
| 136 | <code>    return {&quot;message&quot;: &quot;Book stock reduced&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reduce_book_stock` অংশে |
