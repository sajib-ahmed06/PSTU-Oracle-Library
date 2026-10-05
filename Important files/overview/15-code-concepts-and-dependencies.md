# Code concepts, dependencies ও পড়ার সহায়ক glossary

## Python

`Path(__file__).resolve()` current file-এর absolute path; `.parent` দিয়ে project root। Environment os.environ process config। subprocess.run SQLPlus process launch, stdin input, stdout/stderr capture, returncode ও timeout। Exceptions flow-তে HTTPException request error; subprocess.TimeoutExpired wait limit। `dict(zip(keys,values))` row values-এর নাম দেয়। `parse_qs` URL-encoded keys parse করে। Regex fullmatch entire field rule enforce; re.search malformed percent search করে।

`async def` coroutine; await cooperative operations; synchronous subprocess async function-এর ভেতরে চালালে event loop block হতে পারে। starlette.run_in_threadpool login-এর blocking callback worker thread-এ চালায়। ContextVar current request actor আলাদা context-এ রাখে; token/reset পূর্বের value restore করে।

FastAPI decorators HTTP verb/path handler map করে; typed Request framework request object; integer path/query parameters framework convert করে। APIRouter auth route grouping। FileResponse file response, RedirectResponse 303 navigation, JSONResponse headers/cookie controllable JSON; StaticFiles assets। Middleware endpoint-এর আগে/পরে shared checks।

secrets cryptographic randomness, hashlib PBKDF2, hmac constant-time comparison, base64 serialized binary bytes। time.time epoch expiry; JSON loads audit snapshots decode। unittest TestCase assertions; mock.patch isolates SQL/fetch-like collaborators। tests HTTP server sockets/threading/urllib/http.cookiejar ব্যবহার করে real network/cookie flow isolated test app-এ checks।

## JavaScript ও browser

IIFE `(() => {...})()` script scope আলাদা করে। Destructuring `{ $, state }` helpers নেয়। `$` querySelector; `$$` querySelectorAll spread array। Template literals `${...}` values interpolate; escapeHtml ছাড়া arbitrary user text innerHTML-এ নিরাপদ নয়। textContent plain output। dataset HTML data-* attributes access করে।

Array filter search/eligibility, map rows/options, reduce totals, find target member/book, sort copied loans। Optional chaining ?. missing DOM/property tolerate করে; nullish ?? কেবল null/undefined fallback; || zero/empty string-ও fallback করে। Date/Intl formatting dates/timezone display।

fetch returns Promise; response.ok status class; response.json body decode; async/await then/catch/finally response/error/cleanup। FormData collects named controls; URLSearchParams form body/query বানায়। AbortController signal timeout cancel করে। setTimeout search debounce/toast/login timeout; setInterval reconnect polling। clearTimeout পুরোনো callback বাতিল করে।

onclick/onsubmit/oninput/onchange handlers actions bind; preventDefault browser form navigation আটকায়। disabled repeat clicks কমায়; login explicit submitting flag concurrent request আটকায়। history.replaceState new=1 URL parameter remove করে। Node vm tests JavaScript চালায়, কিন্তু real CSS layout/browser renderer নয়।

## HTML ও CSS

name attribute API form key; id JavaScript selector; label control context; required/pattern/minlength/maxlength browser validation। Hidden student_id target endpoint construction-এ লাগে; backend path ID authoritative। autocomplete username/current-password credential UX; aria-live alerts, aria-hidden dialog visibility, aria-modal/role accessible dialog semantics, aria-pressed password visibility state। Server validation ছাড়া HTML checks bypassable।

CSS variables :root theme tokens। Grid/Flexbox layout, minmax/clamp responsive sizing, overflow-x tables, z-index dialogs/toasts। backdrop-filter underlying photo blur; semi-transparent rgba tint; box-shadow depth; border-radius glass card shape। :focus-visible keyboard indication; :autofill vendor override saved text contrast; @media viewport breakpoints; @supports feature fallback; prefers-reduced-motion shared styles movement কমায়।

## Oracle / SQLPlus

SQL DDL CREATE/ALTER/DROP schema objects বদলায়; implicit commit গুরুত্বপূর্ণ। DML INSERT/UPDATE/DELETE transaction data বদলায়। SELECT INTO PL/SQL single-row variable assignment; no row NO_DATA_FOUND; multiple rows TOO_MANY_ROWS। FOR UPDATE locks matched row until transaction end। COMMIT persists, ROLLBACK business/audit rows undo; NEXTVAL allocation undo হয় না।

Triggers :NEW/:OLD row pseudo-records; INSERTING/UPDATING/DELETING branch event type; AFTER audit versus BEFORE identity/inventory checks। RAISE_APPLICATION_ERROR -200xx custom messages। SQL%ROWCOUNT affected rows। NVL Oracle null fallback; TRIM/UPPER/LOWER normalization; || concatenation; CHR escape-building; RAWTOHEX binary-safe transport; TO_CHAR date/number formatting; ROWNUM older pagination। Oracle empty string NULL semantics identity validation-এ প্রভাব ফেলে।

SQLPlus SET DEFINE OFF ampersand variable substitution বন্ধ; / PL/SQL buffer execute; @@ relative script include; WHENEVER SQLERROR fail-fast; PROMPT progress। PL/SQL %TYPE column datatype reuse করে; procedures business operations, function reusable return value, view reusable SELECT, index uniqueness/search, sequence key allocation।
