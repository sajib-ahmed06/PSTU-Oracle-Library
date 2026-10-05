"""Generate source-backed Bengali project documentation without importing the app."""

import ast
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
DATE = "2026-10-04"

PURPOSES = {
    "backend/main.py": "FastAPI application তৈরি, authentication middleware বসানো, HTML page দেওয়া এবং library API পরিচালনা করে। SQL transport ও validation আলাদা module থেকে ব্যবহার করে।",
    "backend/database.py": "Environment ও .env থেকে database configuration নেয়; SQL*Plus subprocess দিয়ে Oracle SQL চালায়; errors-কে HTTP status-এ রূপান্তর এবং delimiter-separated rows-কে dictionaries-এ decode করে।",
    "backend/validation.py": "URL-encoded form parsing, required fields, integer, text length, academic IDs এবং member contact তথ্য যাচাই করে।",
    "backend/audit.py": "ContextVar-এ request actor রাখে; একই request-এর database কাজ কে করছে সেই পরিচয় Oracle session-এ পাঠানোর ব্যবস্থা করে।",
    "backend/setup_database.py": "Windows SQL*Plus দিয়ে SYSDBA/bootstrap, sample database reset অথবা existing database migration চালায়।",
    "backend/auth/routes.py": "Login, logout, current session, librarian account management এবং administrator credentials change endpoints নিবন্ধন করে।",
    "backend/auth/session.py": "In-memory session token সৃষ্টি/expiry/invalidation, admin permission, request origin check এবং protected resource access নিয়ন্ত্রণ করে।",
    "backend/auth/passwords.py": "Salted PBKDF2 password hashes তৈরি ও verify করে; legacy plaintext management passwords-ও login-এর সময় verify করতে পারে।",
    "backend/auth/__init__.py": "Auth package-এর public helper functions re-export করে।",
    "backend/requirements.txt": "FastAPI এবং Uvicorn dependencies ঘোষণা করে; বর্তমানে version pin করা নেই।",
    "backend/oracle_config/tnsnames.ora": "XE alias-কে localhost TCP port 1521 এবং XE service-এর সঙ্গে যুক্ত করে।",
    "backend/oracle_config/sqlnet.ora": "Application connection-এর Windows OS authentication বন্ধ রাখে। Setup-এর স্থানীয় SYSDBA path এই TNS configuration বাদ দেয়।",
    "database/bootstrap.sql": "CONFIGURED_SCHEMA user তৈরি অথবা তার password reset/unlock করে এবং schema তৈরির privileges দেয়।",
    "database/setup.sql": "Existing library objects drop করে demo schema, sequences, triggers, procedures, view এবং sample records তৈরি করে। শেষে members/audit upgrade অন্তর্ভুক্ত করে।",
    "database/migrate.sql": "Existing records না মুছে sequence advance, case-insensitive indexes ও member/audit upgrade চালায় এবং invalid objects পরীক্ষা করে।",
    "database/members_audit.sql": "Roll/registration fields ও uniqueness, student identity validation, transactional audit triggers এবং initial snapshots তৈরি করে।",
    "frontend/shared.js": "সব management page-এর shared API client, state, header, navigation, live data loader, reconnection monitor, escaping, modal ও form submission helpers।",
    "frontend/login.js": "Password show/hide, single pending login request, username trim, timeout, response validation এবং successful redirect পরিচালনা করে।",
    "frontend/dashboard.js": "Books, copies, loans, members ও fines-এর overview metrics এবং recent loans render করে।",
    "frontend/books.js": "Book search, inventory rows, restock এবং available stock reduction forms পরিচালনা করে।",
    "frontend/students.js": "Member directory ও search; add, full Edit এবং membership enable/disable actions চালায়।",
    "frontend/circulation.js": "Eligible member search, available book selection, issuing, return এবং loan status filter পরিচালনা করে।",
    "frontend/fines.js": "Fine totals, unpaid/paid history এবং mark-paid action পরিচালনা করে।",
    "frontend/accounts.js": "Administrator-এর librarian create/toggle/delete এবং নিজের credentials change forms চালায়।",
    "frontend/audit.js": "Admin audit search, filters, pagination এবং before/after details modal render করে।",
    "frontend/login.css": "Photo background, translucent glass login card, autofill readability, focus indication ও responsive sign-in layout।",
    "frontend/styles.css": "Management pages-এর shared design tokens, header, navigation, tables, metrics, forms, dialogs এবং responsive styles।",
    "run.ps1": "Project directory-তে গিয়ে dependencies import check/install করে localhost:8091-এ Uvicorn চালায়।",
    "Open-Library-Project.bat": "Minimized PowerShell server launcher শুরু করে আট সেকেন্ড পরে browser-এ localhost:8091 খোলে।",
    "Setup-Database.bat": "Database setup Python script চালিয়ে success/failure দেখায় এবং window খোলা রাখে।",
    ".env.example": "Public database configuration template; real private .env values-এর পরিবর্তে এটি document করা হয়েছে।",
    ".gitignore": "Private .env, virtual environments, caches, logs এবং local database backups version control থেকে বাদ দেওয়ার তালিকা।",
    ".vscode/settings.json": "Local VS Code Python interpreter ও Pylance import search paths configure করে। Paths এই computer-এর জন্য নির্দিষ্ট।",
    "README.md": "Project চালানো, database upgrade, structure, login flow, member identifiers ও audit সম্পর্কে মূল usage guide।",
    "overview/tools/generate_docs.py": "এই documentation-এর generator: source inventory, API extraction, function/line explanation, complete code copies এবং SHA-256 manifest তৈরি করে। App import বা database mutation করে না।",
}

FUNCTIONS = {
    "settings": ".env থাকলে key=value lines পড়ে; process environment দিয়ে override করে। .env না থাকলে environment-এর copy ফেরত দেয়।",
    "quote": "SQL string literal-এর apostrophe দ্বিগুণ করে এবং control characters reject করে। এটি prepared/bind query নয়; SQL*Plus string construction helper।",
    "run_sql": "Single shared SQL slot নিয়ে Oracle client subprocess চালায়; handler cleanup-এর জন্য 150ms বিরতি দেয়। CONNECT success marker দিয়ে SQL execution শুরু হয়েছে কি না বোঝে; transient connection errors সর্বোচ্চ দুইবার retry। Read-only SELECT known disconnect errors-ও retry করে, executed writes/timeouts replay করে না। Actor, substitution off, rollback ও 20-second command timeout বজায় থাকে।",
    "rows": "SQL execute করে প্রতিটি nonblank line-কে | delimiter দিয়ে ভাগ করে keys-এর সঙ্গে মেলায়; ~ null marker এবং নির্দিষ্ট numeric fields decode করে। Unexpected field count হলে 502।",
    "execute_dml": "DML statement-এর শেষে semicolon এবং COMMIT যোগ করে একই SQL*Plus execution-এ চালায়।",
    "form_data": "Request body পড়ে 16 KiB ও 30-field সীমা যাচাই করে। UTF-8, percent encoding ও duplicate keys যাচাই করে URL-encoded values-এর dictionary ফেরত দেয়।",
    "required": "প্রয়োজনীয় fields absent, None অথবা whitespace-only হলে HTTP 400 তোলে।",
    "positive_number": "int conversion-এর পরে value অন্তত 1 কি না দেখে। Form strings-এর fractional input int conversion-এ reject হয়।",
    "text_field": "Whitespace trim করে UTF-8 byte length ও control characters যাচাই করে normalized text ফেরত দেয়।",
    "academic_identifier": "Identifier uppercase করে সর্বোচ্চ 40 bytes এবং letters/digits/dot/slash/underscore/hyphen pattern যাচাই করে; leading zero বজায় থাকে।",
    "member_details": "নাম, department, phone, email, roll ও registration একসঙ্গে normalize/validate করে; email lowercase এবং phone ঠিক 11 ASCII digits হতে হয়।",
    "hash_password": "16-byte random salt এবং 260000 PBKDF2-HMAC-SHA256 rounds দিয়ে digest তৈরি করে; salt/digest Base64-এ serialize করে।",
    "verify_password": "Legacy value হলে constant-time comparison; hash হলে format/rounds/salt decode করে PBKDF2 পুনরায় চালিয়ে compare করে। Malformed storage false ফেরায়।",
    "current_session": "Cookie token দিয়ে SESSIONS dictionary lookup করে; expired session সরিয়ে None ফেরায়। Valid session হলে তার dictionary ফেরায়।",
    "require_admin": "Session না থাকলে অথবা role ADMIN না হলে HTTP 403; valid admin session ফেরত দেয়।",
    "create_session": "Expired tokens cleanup করে cryptographically random token তৈরি করে; user_id, username, role ও আট ঘণ্টার expiry dictionary-তে রাখে।",
    "remove_session": "নির্দিষ্ট token dictionary থেকে সরিয়ে logout/invalidation করে।",
    "invalidate_user_sessions": "এক user_id-এর সব session token খুঁজে সরায়; disabled/deleted account অথবা credential change-এ ব্যবহৃত।",
    "install_authentication": "HTTP middleware register করে যাতে route execution-এর আগেই authentication/origin checks হয়।",
    "require_authentication": "Public paths নির্ধারণ করে; write request-এর supplied Origin-এর scheme/host যাচাই করে; request actor context বসায়; private API-তে 401, page-এ login redirect দেয়; nonstatic response-এ no-store।",
    "register_auth_routes": "Injected rows/execute_dml/quote/form helpers ব্যবহার করে APIRouter-এ auth/account routes define ও app-এ include করে।",
    "login_page": "Session থাকলে dashboard redirect; না থাকলে login.html FileResponse দেয়।",
    "login": "Form parse ও length check করে authenticate helper worker thread-এ চালায়; পুরোনো cookie session সরিয়ে নতুন HttpOnly SameSite=strict cookie দেয়। HTTPS হলে Secure flag।",
    "authenticate": "Username দিয়ে Oracle user খোঁজে, password/role/status যাচাই করে এবং প্রয়োজন হলে legacy plaintext password hash-এ upgrade করে; সেই upgrade-এর audit actor user-এর username হয়।",
    "auth_session": "Current session থেকে username ও user_type JSON দেয়; session না থাকলে 401।",
    "logout": "Cookie token invalidates করে browser cookie delete response দেয়।",
    "get_accounts": "Admin permission যাচাই করে admin/librarian account metadata ফেরায়; passwords select করে না।",
    "create_librarian": "Admin-only username/password validation, duplicate check ও hashed password insertion করে; role LIBRARIAN এবং status ACTIVE।",
    "toggle_librarian": "Admin-only target librarian status পরিবর্তন করে; disabled হলে তার active sessions সরিয়ে দেয়।",
    "delete_librarian": "Admin-only librarian যাচাই করে delete করে এবং তার sessions invalidates করে। Admin account এই helper দিয়ে delete হয় না।",
    "change_admin_credentials": "Current password verify করে নতুন username/password validate ও update করে; অন্য sessions বাতিল করে current token-এর session ধরে রাখে।",
    "validate_credentials": "Username letter দিয়ে শুরু, 3–30 characters এবং letters/digits/underscore; password 4–128 characters হতে হয়।",
    "username_exists": "Case-insensitive username count query চালায়; current user-এর ID বাদ দেওয়া যায় যাতে নিজের username রাখা সম্ভব হয়।",
    "librarian": "Target user LIBRARIAN কি না query করে; absent হলে 404।",
    "home": "Dashboard index.html response দেয়; authentication middleware আগেই access check করে।",
    "books_page": "Books page HTML পরিবেশন করে।",
    "students_page": "Members directory HTML পরিবেশন করে।",
    "circulation_page": "Issue/Return page HTML পরিবেশন করে।",
    "fines_page": "Fine register HTML পরিবেশন করে।",
    "accounts_page": "ADMIN role ছাড়া dashboard redirect দেয়; admin হলে accounts.html দেয়।",
    "health": "dual-এ SELECT 1 চালিয়ে actual Oracle connectivity যাচাই করে CONNECTED metadata দেয়। এটি public endpoint।",
    "get_books": "book_details view থেকে title/author/category search ও available/total stock ফেরায়। Search SQL LIKE হওয়ায় % ও _ wildcard হতে পারে।",
    "add_book": "Form validate করে author/category resolve বা create করে; matching book row lock করে restock, নয়তো নতুন title insert; transaction শেষে commit।",
    "reduce_book_stock": "Book lock করে requested quantity available stock ছাড়িয়েছে কি না দেখে; total ও available উভয় count কমায়। Borrowed copies বাদ দেওয়া যায় না।",
    "get_students": "Member directory ফেরায়; generated student_id, contact/status এবং separate roll_no/registration_no fields থাকে।",
    "add_student": "Shared member validation ও existing phone check করে সাত argument-সহ add_student_proc চালায়; identity trigger ও unique indexes final integrity enforce করে।",
    "edit_student": "পুরো member details ও membership_status validate করে; target row lock করে disabling-এর loan/fine restrictions checks; সব editable fields এক transaction-এ update করে।",
    "update_student_identity": "Compatibility endpoint: শুধু roll ও registration update করে; missing row-তে 404 mapping-এর জন্য NO_DATA_FOUND তোলে। Current UI full edit endpoint ব্যবহার করে।",
    "toggle_student_membership": "Member lock করে ACTIVE থেকে DISABLED যাওয়ার আগে active loans/unpaid fines দেখে; DISABLED হলে ACTIVE করে।",
    "get_issues": "Loan, student ও book join করে issue/due/return dates এবং status JSON rows দেয়; newest issue আগে।",
    "add_issue": "Student ও book IDs positive integer যাচাই করে issue_book_proc call এবং commit করে।",
    "return_book": "Positive issue ID নিয়ে return_book_proc call করে; returned inventory/fine changes এক transaction-এ commit।",
    "get_fines": "Fine, issue, student ও book join করে amount ও payment status দেখায়।",
    "pay_fine": "Target fine PAID update করে; affected row না থাকলে NO_DATA_FOUND; audit trigger-সহ commit করে। Already-paid row আবার update করলেও নতুন audit event হতে পারে।",
    "get_meta": "Author/category IDs ও names দেয়; book form datalist-এর options হিসেবে ব্যবহৃত।",
    "audit_page": "Admin permission ছাড়া access reject করে; admin-কে audit.html response দেয়।",
    "get_audit": "Admin-only search/entity/action filters ও 25-row Oracle ROWNUM pagination; RAWTOHEX snapshots decode করে JSON before/after ফেরায়। Stored UTC timestamps UI-তে Dhaka সময় হয়।",
    "oracle_environment": "Oracle home/SID/client language/PATH বসায় এবং proxy settings বাদ দেয়; local SYSDBA mode-এ TNS_ADMIN বাদ দেয়।",
    "execute": "SQL*Plus /nolog subprocess-এ CONNECT এবং script পাঠায়; 120-second timeout/OS errors friendly failure message দেয়; command-line arguments-এ password দেয় না।",
    "main": "এই file-এর entry point; setup/migration flags বা test launcher অনুযায়ী প্রয়োজনীয় workflow শুরু করে। setup_database.py-এর main-এ --migrate preserving upgrade, অন্যথায় RESET confirmation-সহ demo setup।",
    "api": "Relative /api URL-এ no-store fetch, 60-second timeout এবং temporary GET 503/504/network failure-এ একবার retry। POST/DELETE replay হয় না। 401 login redirect, অন্য failed status Error।",
    "escapeHtml": "& < > quote/apostrophe-কে HTML entities বানায় যাতে user-controlled values template HTML হিসেবে execute না হয়।",
    "memberId": "Internal numeric ID-কে display-only PSTU-0001 format-এ বানায়; academic roll/reg-এর সঙ্গে এক নয়।",
    "table": "Headers ও row HTML দিয়ে table বানায়; rows খালি হলে empty-state message দেয়। Calling code-কে values escape করতে হয়।",
    "toast": "Toast textContent/class বদলায় এবং পুরোনো timer clear করে প্রায় 2.8 seconds পরে message লুকায়।",
    "renderHeader": "Navigation, connection indicator, session user ও logout button বসায়; Accounts/Audit links শুধু ADMIN-এর জন্য visible হয়।",
    "setConnection": "Connection dot/label update করে; offline অবস্থায় Database unavailable দেখায়।",
    "loadData": "Overlapping refresh একই pending Promise share করে। Redundant initial health বাদ দিয়ে পাঁচ read API আনে; all-or-nothing state update, failure-এ retained data ও offline writes block; render ও reconnect monitor শুরু।",
    "startConnectionMonitor": "5-second interval-এ health পরীক্ষা; hidden/pending check/data load skip। Reconnect-এ state reload; browser online ও visibilitychange recovery handlers-ও থাকে।",
    "sortIssues": "Issue date descending ও তারপর numeric issue ID descending-এ copied list sort করে।",
    "issueRows": "Loan table HTML render করে; active loan-এর due date পেরোলে OVERDUE label; actions enabled হলে Return button।",
    "openModal": "Dialog open করে aria attributes বসায়, return-focus element ধরে এবং প্রথম input/select/button-এ focus দেয়।",
    "closeModal": "Dialog hide করে form reset ও opener focus restore করে।",
    "bindModals": "Open/close/backdrop/Escape handlers এবং Tab/Shift+Tab focus containment বসায়।",
    "postForm": "Offline হলে save আটকায়; submit button disable করে URLSearchParams(FormData) POST; success-এ modal close ও toast; শেষে button restore। Login-এর মতো আলাদা submitting flag এখানে নেই।",
    "openRequestedModal": "URL-এর new=1 থাকলে requested dialog খুলে query parameter সরায়; reconnection-এ dialog পুনরায় খোলা বন্ধ হয়।",
    "render": "এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।",
    "openRestock": "Existing book metadata form-এ ভরে quantity=1 দেয়, modal open করে এবং quantity select করে।",
    "openReduction": "Book ID/form max available copies বসিয়ে reduction modal খোলে।",
    "toggleMembership": "User confirmation ও online check-এর পরে member toggle API call, toast ও fresh render।",
    "eligibleStudents": "ACTIVE members-এর মধ্যে active loan বা unpaid fine নেই এমন members নির্বাচন করে। Database procedure আবার একই rules enforce করে।",
    "renderMembers": "Eligible members-এর name/internal ID/roll/reg search করে select options render করে; no match হলে empty option।",
    "returnBook": "Confirmation-এর পরে return API call ও refreshed data render করে।",
    "payFine": "Confirmation-এর পরে mark-paid API call ও refreshed fines render করে।",
    "renderAccounts": "Admin account list fetch করে role/status/action rows render এবং toggle/delete button handlers বসায়।",
    "submitForm": "Accounts page form-এর submit button disable করে POST, successful form reset ও toast করে; finally button restore।",
    "toggleAccount": "Confirmation নিয়ে librarian account toggle API call এবং account list refresh করে।",
    "deleteAccount": "Permanent delete confirmation নিয়ে librarian deletion API call এবং list refresh করে।",
    "loadAudit": "Filters/page থেকে query বানায়, request counter দিয়ে stale responses ignore করে, table ও pagination render করে; row detail buttons bind করে।",
    "showDetails": "Selected audit event-এর before/after keys union করে comparison table বানায়; changed fields highlight করে modal খোলে।",
}

CHAPTERS = {
    "14-data-dictionary-and-responses.md": """# প্রতিটি database field ও API response

নিচের dictionary current final schema বোঝায়। PK = primary key; FK = foreign key; legacy fields UI authentication-এর সঙ্গে যুক্ত নয়। VARCHAR2 length Oracle default byte semantics-এ তৈরি; Python input validator UTF-8 bytes checks করে।

| Table.field | Type | Meaning / rule |
| --- | --- | --- |
| admin.admin_id | NUMBER PK | admin_seq/trigger-generated legacy profile identity |
| admin.name | VARCHAR2(100) NOT NULL | Profile name |
| admin.email | VARCHAR2(100) NOT NULL UNIQUE | Profile email |
| admin.password | VARCHAR2(255) NOT NULL | Legacy password; current login source নয়; audit থেকে বাদ |
| student.student_id | NUMBER PK | student_seq-generated internal identity; roll/reg নয় |
| student.name | VARCHAR2(100) NOT NULL | Member display name; unique নয় |
| student.department | VARCHAR2(100) NOT NULL | Member department |
| student.phone | VARCHAR2(11) NOT NULL UNIQUE | ঠিক 11 numeric digits; leading zero string হিসেবে রাখা |
| student.email | VARCHAR2(100) NOT NULL UNIQUE | Contact email; normalized index LOWER(TRIM(email)) |
| student.password | VARCHAR2(255) NOT NULL | Legacy unused member password; add route default '<private-password>'; audit থেকে বাদ |
| student.membership_status | VARCHAR2(20) DEFAULT ACTIVE NOT NULL | ACTIVE অথবা DISABLED; borrowing permission |
| student.roll_no | VARCHAR2(40) | ID/Roll; UPPER(TRIM()) unique index; new inserts/ID edits trigger-required |
| student.registration_no | VARCHAR2(40) | Registration No.; independently UPPER(TRIM()) unique; leading zeros রাখে |
| author.author_id | NUMBER PK | author_seq/trigger identity |
| author.author_name | VARCHAR2(100) NOT NULL UNIQUE | Normalized LOWER(TRIM()) index-সহ author name |
| category.category_id | NUMBER PK | category_seq/trigger identity |
| category.category_name | VARCHAR2(100) NOT NULL UNIQUE | Normalized LOWER(TRIM()) index-সহ category name |
| book.book_id | NUMBER PK | book_seq/trigger title identity |
| book.title | VARCHAR2(200) NOT NULL | Title; normalized title+author+category uniqueness |
| book.author_id | NUMBER NOT NULL FK | References author.author_id |
| book.category_id | NUMBER NOT NULL FK | References category.category_id |
| book.publisher | VARCHAR2(100) | Optional publisher; API empty input defaults PSTU Library |
| book.quantity | NUMBER DEFAULT 0 NOT NULL | Total stock; database check ≥0; API whole positive count add/reduce |
| book.available_quantity | NUMBER DEFAULT 0 NOT NULL | Available stock; 0≤available≤quantity |
| issue_book.issue_id | NUMBER PK | issue_seq/trigger loan identity |
| issue_book.student_id | NUMBER NOT NULL FK | References student.student_id |
| issue_book.book_id | NUMBER NOT NULL FK | References book.book_id |
| issue_book.issue_date | DATE DEFAULT SYSDATE NOT NULL | Borrowing timestamp; read API YYYY-MM-DD format |
| issue_book.due_date | DATE | Procedure/trigger normal issue-date rule: issue date+15 days |
| issue_book.return_date | DATE | Return timestamp; active loan হলে null |
| issue_book.status | VARCHAR2(20) DEFAULT ISSUED NOT NULL | ISSUED অথবা RETURNED |
| return_book.return_id | NUMBER PK | return_seq/trigger return identity |
| return_book.issue_id | NUMBER NOT NULL UNIQUE FK | একটি issue-এর একটি return; references issue_book |
| return_book.return_date | DATE DEFAULT SYSDATE NOT NULL | Completed return time |
| return_book.fine_amount | NUMBER DEFAULT 0 NOT NULL | Computed fine, ≥0; zero fine-ও return history-তে থাকে |
| return_book.status | VARCHAR2(20) DEFAULT RETURNED NOT NULL | Stored return label; table-এ separate domain CHECK নেই |
| fine.fine_id | NUMBER PK | fine_seq/trigger fine identity |
| fine.issue_id | NUMBER NOT NULL UNIQUE FK | প্রতি issue-এর সর্বোচ্চ একটি fine |
| fine.amount | NUMBER DEFAULT 0 NOT NULL | Nonnegative amount; return procedure daily late charge×10 |
| fine.payment_status | VARCHAR2(20) DEFAULT UNPAID NOT NULL | UNPAID অথবা PAID |
| login_user.user_id | NUMBER PK | login_seq/trigger management account identity |
| login_user.username | VARCHAR2(100) NOT NULL UNIQUE | Database allows 100 bytes; create/change API rule 3–30 chars; normalized unique index |
| login_user.password | VARCHAR2(100) NOT NULL | PBKDF2 serialized value অথবা legacy plaintext; never account-list/audit response field |
| login_user.user_type | VARCHAR2(20) NOT NULL | ADMIN, LIBRARIAN অথবা STUDENT; dashboard login প্রথম দুইটি |
| login_user.account_status | VARCHAR2(10) DEFAULT ACTIVE NOT NULL | ACTIVE অথবা DISABLED |
| audit_log.audit_id | NUMBER PK | audit_seq; event ordering/key |
| audit_log.occurred_at | TIMESTAMP NOT NULL | SYS_EXTRACT_UTC(SYSTIMESTAMP) insertion time; UI Dhaka conversion |
| audit_log.actor | VARCHAR2(100) NOT NULL | Request username / Oracle USER / initial MIGRATION label |
| audit_log.action | VARCHAR2(10) NOT NULL | INSERT, UPDATE, DELETE, SNAPSHOT |
| audit_log.entity | VARCHAR2(30) NOT NULL | Uppercase table name; no target table FK |
| audit_log.record_id | NUMBER NOT NULL | Target row primary key; entity ছাড়া global unique নয় |
| audit_log.before_data | VARCHAR2(4000) | JSON old values; INSERT/SNAPSHOT-এ null; secret fields excluded |
| audit_log.after_data | VARCHAR2(4000) | JSON new values; DELETE-এ null; secret fields excluded |

## Read response schemas

- GET books: array of book_id, title, author_name, category_name, publisher, quantity, available_quantity। IDs/counts numeric; missing publisher null হতে পারে।
- GET students: array of student_id, name, department, phone, email, membership_status, roll_no, registration_no। Academic IDs strings; unknown legacy IDs null। Student password ফেরত আসে না।
- GET issues: array of issue_id, student_id, book_id, student, title, issue_date, due_date, return_date, status। Dates YYYY-MM-DD; due/return missing হলে null।
- GET fines: array of fine_id, issue_id, student_id, student, title, amount, payment_status। amount Python int অথবা decimal-output float।
- GET meta: object authors/categories, each array contains id/name।
- GET accounts: user_id, username, user_type, account_status array; passwords নেই।
- GET audit: items,total,page,page_size। Item audit_id,occurred_at,actor,action,entity,record_id,before,after। before/after dictionaries অথবা null।
- Login/current session: username,user_type। Login token JSON-এ নয়, cookie-তে।
- Mutation endpoints সাধারণত message object দেয়; new member/book/issue ID response-এ নেই, frontend rereads lists। Credential change username-ও ফেরায়।
- Errors: FastAPI HTTPException response সাধারণত detail string। Server framework request conversion errors detail array হতে পারে; shared API helper সব detail shapes-এর friendly formatting করে না।

## Sample request

```text
POST /api/students
Content-Type: application/x-www-form-urlencoded

name=Example&department=CSE&phone=01799999001&email=example%40example.invalid&roll_no=2300010&registration_no=11709
```

এটি documentation example; database-এ insert করা হয়নি। Existing unique values-এর সঙ্গে conflict হলে request 409 হবে। New member-এর academic IDs স্বয়ংক্রিয় sequence fill হয় না—form থেকে দিতে হয়।
""",
    "15-code-concepts-and-dependencies.md": """# Code concepts, dependencies ও পড়ার সহায়ক glossary

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
""",
    "01-project-and-architecture.md": """# Project ও architecture

এই application PSTU Central Library-এর staff management portal। Frontend plain HTML/CSS/JavaScript; backend FastAPI; HTTP server Uvicorn; persistence Oracle XE 10g। ORM অথবা JavaScript build pipeline নেই। Backend Python SQL string বানিয়ে installed Windows SQL*Plus subprocess চালায়।

```mermaid
flowchart LR
  Browser[Browser: HTML/CSS/JS] -->|fetch /api + session cookie| API[Uvicorn + FastAPI]
  API --> Auth[Authentication middleware]
  Auth --> Routes[Route handlers + validation]
  Routes --> SQL[database.py: SQLPlus subprocess]
  SQL --> Oracle[(Oracle XE)]
  Oracle --> Triggers[Inventory + identity + audit triggers]
  Triggers --> History[(audit_log)]
```

Browser প্রথমে HTML ও /static assets নেয়। shared.js header/session check করে; management pages loadData দিয়ে books, students, issues, fines ও meta নেয়। Changes POST/DELETE endpoints দিয়ে যায়। Server validation ও Oracle constraints দুটোতেই checks থাকে। Successful DML এবং তার audit একই transaction-এ commit হয়। Response আসলে page data reload করে।

Directory দায়িত্ব: backend = request/application logic; backend/auth = authentication/accounts; database = bootstrap/reset/migrations; frontend = UI; tests = backend/HTTP/JS checks; overview = এই documentation।

Internal student_id, display PSTU member ID, academic roll এবং registration আলাদা। Display ID database-তে নতুন column নয়; memberId() দিয়ে বানানো হয়। Book quantity total physical stock; available_quantity issue করার মতো copies। Loan issue_book table-এ, completed return return_book-এ, monetary fine fine-এ থাকে।

Documentation current source snapshot-এর ব্যাখ্যা, production security certification নয়। Runtime data বদলালে source একই থেকেও directory/counts বদলাতে পারে।
""",
    "02-setup-and-configuration.md": """# Setup, configuration ও launcher

1. Oracle XE service/listener ও SQL*Plus install থাকতে হবে। Default home `C:\\oraclexe\\app\\oracle\\product\\10.2.0\\server`। `ORACLE_HOME` environment variable দিয়ে override হয়।
2. `python -m pip install -r backend/requirements.txt` চালাও। Python environment-এ FastAPI/Uvicorn থাকতে হবে; tests অতিরিক্ত httpx লাগে না।
3. `.env.example` থেকে `.env` তৈরি করো। DB_USER, DB_PASSWORD, DB_DSN database.py পড়ে। Process environment file values-এর ওপর priority পায়। Current parser পুরো dotenv specification নয়; quotes/export/multiline syntax বিশেষভাবে support করে না। ORACLE_HOME process environment থেকে path তৈরি হওয়ার সময় পড়া হয়, .env-এর ORACLE_HOME দিয়ে path override হয় না।
4. Existing database হলে `python backend/setup_database.py --migrate`। Upgrade sequence advance ও indexes/features যোগ করে; existing library records delete করে না। Oracle DDL implicit commit হয়; failure-এ earlier DDL rollback হয় না। Script idempotent column/index checks রাখে, কিন্তু backup ছাড়া migration undo সুবিধা নেই।
5. Demo reset হলে `Setup-Database.bat`; RESET type করা আবশ্যক। Existing library tables/audit history মুছে sample records ফেরত আসে। Bootstrap existing CONFIGURED_SCHEMA password-ও public demo default-এ reset/unlock করে। Custom schema credentials নিয়ে demo setup স্বয়ংক্রিয় parameterized নয়।
6. `powershell -ExecutionPolicy Bypass -File run.ps1` অথবা launcher batch। Server `127.0.0.1:8091`-এ single worker। Browser URL `http://localhost:8091`। Batch আট সেকেন্ড wait করে; server readiness polling নয়।

tnsnames.ora-তে XE = TCP 127.0.0.1:1521 / service XE / dedicated server। sqlnet.ora application connections-এ OS authentication NONE; setup local SYSDBA attempt TNS_ADMIN বাদ দেয়। NLS_LANG WE8MSWIN1252; Bengali/Unicode data preservation নিশ্চিত করা হয়নি।

Login demo seed <private-administrator-login>; সেটি current account password-এর নিশ্চয়তা নয়, কারণ Accounts page দিয়ে password বদলানো যায়। এই public seed value source-এ আছে; real private .env এই documents-এ নেই।

`.vscode/settings.json` installed interpreter এবং site-packages path ধরে Pylance resolve করে। অন্য PC-তে paths বদলাতে হবে। Browser এক origin-এ রাখো: localhost ও 127.0.0.1 আলাদা cookie hosts।
""",
    "03-backend-and-validation.md": """# Backend ও input validation

main.py creates FastAPI, installs authentication, registers feature routers and mounts frontend assets. backend/routes separates pages, books, members, circulation, fines, snapshot and audit. Authentication routes live under backend/auth; reservations.py provides member-scoped dashboard data and reservation operations. Staff account management and audit require ADMIN access.

Form content frontend থেকে URLSearchParams(new FormData(form)) হয়। form_data request.body সম্পূর্ণ পড়ে, তারপর 16384-byte limit checks; এটি streaming upload size enforcement নয়। সর্বোচ্চ 30 fields; invalid raw/percent-encoded UTF-8, malformed % escapes ও duplicate keys reject। JSON/multipart parsing helper নয়। required() None/blank/whitespace reject করে। positive_number integer ও >0 চায়। text_field সর্বোচ্চ UTF-8 byte length checks; এটি Oracle character-set bytes-এর সরাসরি measurement নয়।

member_details name/department/email সর্বোচ্চ 100 bytes; email lowercase + simple structural regex; phone ঠিক 11 ASCII digits; roll ও registration uppercase, সর্বোচ্চ 40 bytes, allowed ASCII letters/digits/dot/slash/underscore/hyphen। Domain deliverability, country-specific email policy বা unique name requirement নেই।

Add member-এ phone precheck থাকে, তবে race-safe uniqueness Oracle indexes/constraints enforce করে। Full edit-এ name, department, phone, email, roll/reg, membership_status mandatory। Student row SELECT FOR UPDATE lock হয়; ACTIVE→DISABLED-এর আগে issued books ও unpaid fines checks। Internal student_id edit হয় না। Identity-only endpoint compatibility হিসেবে আছে; UI এখন full /edit call করে।

database.py SQL*Plus stdin-এ CONNECT ও script পাঠায়; password subprocess argv-তে দেয় না। SET DEFINE OFF ampersand substitution বন্ধ করে; SQLBLANKLINES ON blank SQL lines নেয়। WHENEVER SQLERROR ... ROLLBACK ও OSERROR handling থাকে। quote() apostrophe escape/control-character reject করে; bind variables নেই। SELECT output fields | delimiter, ~ null marker; কিছু values REPLACE দিয়ে | সরায়, audit RAWTOHEX দিয়ে delimiter/newlines এড়ায়।

HTTP errors: input 400, unauthenticated API 401, forbidden admin/role/origin 403, missing database record 404, conflicts/domain rule 409, too-large form 413, malformed row format 502, database failure 503, timeout 504। Missing SQLPlus path বর্তমানে 500। Generic Oracle failures server log-এ যায়; user-কে internal error detail সাধারণত দেওয়া হয় না।

Login and async library mutation SQL work now runs in run_in_threadpool. Some account create/change operations still contain synchronous database work. SQLPlus commands share one slot to avoid XE listener overload.
""",
    "04-authentication-and-security.md": """# Authentication, roles ও sessions

Login flow: username/password form → body validation → username search → password verification → management role ADMIN/LIBRARIAN check → ACTIVE account check → legacy password hash upgrade প্রয়োজনে → session token creation → cookie response → frontend valid username/role response যাচাই করে dashboard redirect। STUDENT account management dashboard access পায় না; student self-service portal নেই।

PBKDF2-HMAC-SHA256: salt = 16 random bytes, iterations = 260000, digest Base64; format `pbkdf2$rounds$salt$digest`। Verification stored rounds 100000–1000000 range check করে। hmac.compare_digest ব্যবহার হয়। Legacy plaintext stored password login-এ verify হওয়ার পরে hash-এ বদলানো হয়। admin/student profile tables-এর unused legacy password fields current authentication source নয়; login_user password authoritative।

Session dictionary process memory-তে: user_id, username, user_type, expires। Cookie library_session; lifetime আট ঘণ্টা; HttpOnly, SameSite=strict; HTTPS request হলে Secure। Restart হলে sessions হারায়। Shared session backend নেই বলে multiple workers ব্যবহার করলে session lookup mismatch হতে পারে। Expired session access অথবা new session creation-এ cleanup হয়। Logout token ও cookie delete করে। Disabled/deleted librarian-এর sessions invalidated। Admin credential update অন্য sessions invalidates করে বর্তমান token পুনরায় stores। Session expiry sliding refresh নয়।

Middleware permits login, member activation, member password recovery, health and static assets without an authenticated session. Protected APIs return 401 without a session; protected pages redirect to login. STUDENT sessions can access their own dashboard and reservation operations, while management pages require staff access. Write requests with an Origin header must match the current origin. Authenticated responses use Cache-Control: no-store.

Roles: ADMIN সব management, account controls ও audit; LIBRARIAN library operations, account/audit access নেই; STUDENT management login reject। Frontend hidden link permission enforcement নয়; backend require_admin authoritative। HTML escaping data-as-HTML risk কমায়; audit details passwords/hashes বাদ দেয়।

বর্তমান সীমা: rate limiting/account lockout নেই; password minimum মাত্র চার characters; permission/auth state live database-এ প্রতি request revalidate নয়; direct SQL account disable/delete করলে in-memory sessions immediate invalidated হয় না। TLS deployment/session persistence/production secret provisioning এখানে implemented নয়। Audit schema owner records edit/drop করতে পারে; tamper-proof audit service নয়।
""",
    "05-database-and-business-rules.md": """# Database schema, PL/SQL ও business rules

| Table | Fields ও দায়িত্ব |
| --- | --- |
| admin | admin_id, name, email, password; legacy profile/demo table, management login source নয় |
| student | student_id, name, department, phone, email, password, membership_status, roll_no, registration_no |
| author | author_id, author_name; books-এর author reference |
| category | category_id, category_name; books-এর category reference |
| book | book_id, title, author_id, category_id, publisher, quantity, available_quantity |
| issue_book | issue_id, student_id, book_id, issue_date, due_date, return_date, status |
| return_book | return_id, issue_id unique, return_date, fine_amount, status |
| fine | fine_id, issue_id unique, amount, payment_status |
| login_user | user_id, username, password, user_type, account_status |
| audit_log | audit_id, occurred_at UTC timestamp, actor, action, entity, record_id, before_data, after_data |

```mermaid
erDiagram
  AUTHOR ||--o{ BOOK : writes
  CATEGORY ||--o{ BOOK : classifies
  STUDENT ||--o{ ISSUE_BOOK : borrows
  BOOK ||--o{ ISSUE_BOOK : issued
  ISSUE_BOOK ||--o| RETURN_BOOK : returned
  ISSUE_BOOK ||--o| FINE : charged
```

audit_log ও login_user/student-এর মধ্যে FK নেই। Audit record_id entity অনুযায়ী interpret করতে হয়; target deleted হলেও event থাকে। login_user আর student একই ব্যক্তি হওয়া database FK দিয়ে enforced নয়।

Primary keys NUMBER; *_seq sequences ও BEFORE INSERT triggers ID না দিলে NEXTVAL বসায়। Sequence rollback হয় না: failed/test transactions-এ gaps স্বাভাবিক। migrate.sql পুরোনো MAX(id) registrations-এর পর student_seq current max ছাড়িয়ে নেয়। পরবর্তী inserts table-wide lock ছাড়াই sequence IDs পায়।

Uniqueness: student phone/email; case-insensitive trimmed email; independent UPPER(TRIM(roll_no)) ও UPPER(TRIM(registration_no)); author/category normalized names; normalized username; book identity = LOWER(TRIM(title))+author_id+category_id। একই author/category/title restock হয়। একই নামের members হতে পারে; roll/reg/phone/email আলাদা হতে হয়।

Legacy null IDs রাখা হয় যাতে invented identifiers না বসে। student_identity_trigger new insert বা ID edit-এ দুটো academic identifier required, trim/uppercase এবং allowed pattern checks। Existing member-এর অন্য field-only update এই trigger fire করে না; full edit UI দুটো IDs-ই চায়।

Stock invariant: quantity≥0, available_quantity≥0 ও available≤quantity। Reduce stock available copies-এর বেশি নয়। issue_quantity_trigger book row lock করে unavailable হলে -20001; available এক কমায়; dates defaults প্রয়োজনে বসায়।

issue_book_proc locks the member row and validates ACTIVE membership, unpaid fines and the three-copy allowance. Active reservations count toward that allowance. New loans are due 15 days after the issue date; reserved-copy collection uses the same rule. Copy locks prevent simultaneous circulation of one physical copy.

return_book_proc locks the loan, rejects a second return and calculates max(TRUNC(today)-TRUNC(due_date),0) × Tk 10. It returns the physical copy and records the fine in one transaction. Fine payments record receipts and require the full outstanding balance; legacy partial receipts are preserved.

book_details view author/category names join করে readable inventory rows দেয়। check_book_available function availability string দেয়; current frontend API এই function call করে না। Original setup initially issue_book_proc fine table তৈরি হওয়ার আগে defines করে, পরে compile করে; final invalid-object check প্রয়োজন।

setup.sql includes database/schema modules in dependency order, then feature upgrades and audit triggers before sample records. Academic identifiers and session are defined in schema/members.sql. Setup resets project tables; existing installations use backend.upgrade_circulation instead.
""",
    "06-frontend-and-design.md": """# Frontend pages, styles ও interaction

| Page | Markup | Controller | কাজ |
| --- | --- | --- | --- |
| /login | login.html | login.js | Glass sign-in, password visibility, errors |
| / | index.html | dashboard.js | Overview metrics, recent loans, inventory snapshot |
| /books | books.html | books.js | Search, add/restock, stock reduction |
| /students | students.html | students.js | Directory, Add Member, Edit, membership status |
| /circulation | circulation.html | circulation.js | Eligible member/book issue এবং return |
| /fines | fines.html | fines.js | Outstanding fine totals ও mark paid |
| /accounts | accounts.html | accounts.js | Admin account management |
| /audit | audit.html | audit.js | Admin history filters ও field comparison |

Management pages styles.css + shared.js ব্যবহার করে। login page separate login.css/login.js ব্যবহার করে। scripts markup-এর শেষে load হয় তাই querySelector-এর elements আগে তৈরি থাকে। shared.js একটি IIFE থেকে LibraryApp object ফেরায়; page controller IIFE তার helpers destructure করে। No module bundler/React/state library।

styles.css :root tokens colors/spacing-related reusable values রাখে; header/nav, surfaces, metrics, tables, buttons, modals, forms ও responsive breakpoints আছে। Tables .table-wrap overflow-x:auto; narrow screens-এ wide member fields scroll হয়। Dialog open class toggles display, role/aria-modal/aria-hidden set হয়, Escape/backdrop/cancel close; Tab trap ও focus restoration আছে। Toast aria-live polite।

login.css multiple backgrounds: gradient overlay, pstu-library.jpg, fallback library-dashboard.png। Glass panel translucent gradient/tint, backdrop blur/saturation, border/shadow। No-backdrop-filter browser-এ darker fallback। Autofill text/background override ও Show/Hide button solid background readability বজায় রাখে। Mobile single column; short desktop viewport padding কমে। CSS query versions cache refresh করে, build hashes নয়।

login.js username trim, empty username check, AbortController 30-second timeout, single submitting flag, aria-busy এবং response payload role validation রাখে। Error message textContent; malformed JSON success response redirect হয় না। Show/Hide password type বদলায় এবং aria-pressed/aria-controls update হয়।

shared loadData coalesces overlapping refreshes and loads the complete dataset through /api/snapshot in one Oracle connection. Temporary GET failures retry once; failed loads retain old records and block changes. Recovery polling runs every five seconds, plus online/visibility events. Non-401 session lookup failures show an error instead of forcing login redirect.

Member full Edit-এর visible fields name/department/phone/email/roll/reg/status; hidden student_id endpoint target। Enable/Disable আলাদা quick action-ও থাকে। Save-এর পরে reload হওয়ায় directory ও নতুন page reads updated values দেখায়। Circulation select client-side eligibility filter করে; server final checks রাখে। Search browser state-এ হওয়ায় server read endpoint full list আনে।

The management dashboard shows available copies, active loans, members, active reservations and unpaid balances. Priorities highlight overdue returns, pending pickups and fines. The member dashboard separates catalogue, borrowing, reservations, fines and security. MemberDashboard and ReservationDesk own their views; reservations.js coordinates refresh and shared actions.
""",
    "07-audit-and-transactions.md": """# Audit history ও transaction consistency

members_audit.sql audit_json_value function দিয়ে JSON string escaping করে: backslash, double quote ও control characters Unicode escapes। Null SQL value JSON null; numeric/date values snapshot-এ readable strings হতে পারে। before_data/after_data VARCHAR2(4000), dedicated JSON database datatype নয়।

নয়টি AFTER row triggers student/book/author/category/issue_book/return_book/fine/login_user/admin-এর INSERT/UPDATE/DELETE capture করে। One row change = one event; একটি issue operation inventory update এবং loan insert দুই বা বেশি event তৈরি করে। Audit writes autonomous transaction নয়: business rollback হলে events-ও rollback। Sequence values rollback হয় না।

Middleware session username ContextVar-এ বসায়; worker context propagation থাকে। run_sql DBMS_APPLICATION_INFO.SET_CLIENT_INFO দিয়ে actor Oracle session-এ পাঠায়। Trigger SYS_CONTEXT(USERENV,CLIENT_INFO) পড়ে, absent হলে Oracle USER। Legacy login password upgrade নিজের username actor set করে। Manual agent-request updates USER_REQUEST actor ব্যবহার করতে পারে; এটিকে actual admin username ধরে নেওয়া ঠিক নয়।

Initial records migration-এর সময় SNAPSHOT action-এ current values পায়। Existing event থাকলে সেই entity/record আর snapshot insert হয় না। এটি past edit history reconstruct করে না। Tracking শুরু হওয়ার আগের actions অজানা।

Admin /api/audit q/entity/action/page filters দেয়; query search literal INSTR, %/_ wildcard নয়। Page size 25; nested ROWNUM Oracle 10g pagination। actor ও JSON RAWTOHEX transport করে যাতে | অথবা newline field count না ভাঙে; Python cp1252 decode installed database charset ধরে। occurred_at UTC, frontend en-GB format+Asia/Dhaka display।

Audit detail modal keys union করে before/after পাশে দেখায়, differing fields highlight করে। Snapshots/insert-এর before এবং delete-এর after absent। Member name/contact/roll/reg, stock counts, loan dates/status, fine payments ও account role/status tracked। Password/hash fields বাদ। Password-only UPDATE event থাকতে পারে কিন্তু secret values comparison-এ আসবে না। Login/logout session events database record changes নয়, আলাদা events নেই। No export/retention policy/per-user timeline endpoint implemented।
""",
    "08-operation-walkthroughs.md": """# End-to-end operation walkthroughs

## Add/Edit member

Add button → studentModal fields → students.js submit → postForm POST /students → member_details → phone duplicate precheck → add_student_proc → student sequence/identity/audit triggers → COMMIT → success toast → loadData → member directory। Roll/reg frontend pattern user feedback দেয়; unique indexes concurrent duplicates আটকায়।

Edit button → existing values identityModal-এ fill (internal name legacy হলেও UI title Edit member) → POST /students/{id}/edit → all fields/status validation → member lock → disabling rules প্রয়োজনে → UPDATE → audit before/after → commit → reload। Legacy /identity API এখনও callable; current UI নয়। Duplicate failure form close করে না।

## Add/restock/reduce book

Book form title/author/category/publisher/quantity → positive count/text checks → existing normalized author/category lookup বা create → normalized book lookup lock → quantity ও available একই amount বাড়ানো; না থাকলে new book। Reduce existing row lock করে available sufficient হলে দুই count কমায়। Library-issued copies inventory থেকে বাদ দেওয়া যায় না।

## Issue/return/pay

Frontend eligible members list ACTIVE + no current issued book + no unpaid fine। Book select available>0। POST studentId/bookId → issue proc member lock/check → issue insert → inventory trigger book lock/decrement → audit events → commit। অন্য staff একই stock/member ব্যবহার করলে database locks/checks final decision দেয়।

Return button confirm → issue return endpoint → issue lock/returned check → calendar-day lateness×10 → return row/issue update/inventory restore/fine insert → audit → commit। Fine page Mark paid confirm → PAID update, missing row check → audit → commit। Paid balance member eligibility-তে next reload-এ reflected।

## Accounts ও audit

Admin accounts form username/password confirm → JS passwords match → backend permission/credential rules/uniqueness → hash insert। Disable/delete sessions invalidates। Credentials currentPassword mandatory। Audit navigation visible only admin; API/page permissions separate checks। Detail modal existing event snapshots দেখায়; live current values দিয়ে পুরোনো snapshot overwrite হয় না।
""",
    "09-testing-and-maintenance.md": """# Tests, verification ও maintenance

Python: `python -m unittest discover -s tests -v`। JavaScript: `node --test tests/login.test.cjs tests/members.test.cjs`। Python syntax: `python -m compileall -q backend`। PowerShell JavaScript syntax: `Get-ChildItem frontend -Filter *.js | ForEach-Object { node --check $_.FullName }`।

test_regressions.py password hash/legacy, quoting/control input, forms, session invalidation, row decoding, missing fines ও Oracle error/rollback configuration checks করে। test_login_api.py isolated FastAPI/Uvicorn server + stdlib HTTP cookie client দিয়ে real HTTP workflow checks করে; fake account rows ব্যবহার করে, real Oracle records বদলায় না। Slow login query চলার সময় health response test threadpool behavior checks।

test_members_audit.py member normalization/required IDs/full edit validation, generated SQL/locks/disabling protections, duplicate error messages, admin-only audit, hex/JSON pagination ও actor propagation পরীক্ষা করে। login.test.cjs Node vm-এ DOM/fetch stubs দিয়ে visibility/success/error/repeated submission checks। members.test.cjs directory fields/search checks; browser layout validation নয়।

Source tests-এর কিছু SQL assertions implementation details check করে; এর পাশাপাশি session/API/encoding behavior tests আছে। Live Oracle transactional verification আগের কাজের সময় করা হয়েছে; ordinary test suite সব schema/trigger paths live Oracle-এ স্বয়ংক্রিয় চালায় না। Browser screenshot/visual QA-এর callable browser connection পাওয়া যায়নি। Passing tests সব future bugs নেই এমন guarantee নয়।

Maintenance: new member field হলে validation, form, prefill, API list/create/edit, schema migration ও audit student snapshot বদলাতে হবে। নতুন table audit করতে হলে trigger/snapshot/entity whitelist/frontend labels add করতে হবে। New endpoint permission middleware/require_admin ও frontend navigation দুইটাই review করো। Business rules frontend-only নয়, backend/database-এ রাখো।

Docs refresh: `python 'Important files/overview/tools/generate_docs.py'`। Generator app import/SQL execute করে না; source files read করে overview markdown/index/manifest overwrite করে। Schema/API changes-এর পরে curated chapters manually review করো; generated line/function inventories নতুন source তুলে নেয়, কিন্তু narrative business explanation স্বয়ংক্রিয় semantic proof নয়।
""",
    "10-troubleshooting-and-limitations.md": """# Troubleshooting ও বর্তমান limitations

| Symptom | কারণ/সমাধান |
| --- | --- |
| Pylance FastAPI missing import | VS Code interpreter installed FastAPI environment-এর সঙ্গে মেলাও; .vscode absolute paths local PC-এর; reload language server/window |
| SQLPlus not found | ORACLE_HOME path ও bin/sqlplus.exe check; setup এবং runtime path environment-driven |
| Oracle unavailable | XE service/listener, port 1521, TNS alias এবং DB credentials check; health endpoint actual SELECT চালায় |
| Invalid objects after migration | USER_ERRORS ও USER_OBJECTS inspect; migration recompiles dependent student trigger/issue/return procedures |
| Unique identifier error | অন্য member একই normalized roll/reg ব্যবহার করছে; case বা whitespace বদলিয়ে bypass হয় না |
| Cannot disable membership | Active loan return এবং unpaid fines pay করতে হবে; Edit status ও quick toggle একই rules রাখে |
| Cannot issue another book | Existing loan/unpaid fines/disabled membership/zero stock checks |
| Login loops after restart | Sessions in memory; login আবার করতে হবে; multiworker/shared sessions নেই |
| Background পুরোনো | pstu-library.jpg asset আছে কি না এবং Ctrl+F5; CSS fallback পুরোনো library image |
| UI old Edit IDs | Server restart এবং cache-versioned students.js reload; button current source Edit |
| Audit empty/forbidden | Admin login চাই; filters clear করো; feature migration/app restart check |

সীমাবদ্ধতা source অনুযায়ী: SQLPlus per request subprocess overhead; bind variables/connection pool নেই; dependencies unpinned; in-memory sessions; weak minimum password policy; no rate limiting; legacy unused plaintext fields; Windows/Oracle10g assumptions; Unicode transport legacy charset; no delete-member workflow; no automatic academic-ID sequence assignment for newly added members; no backup scheduler/export/retention; audit schema owner tampering prevention নেই।

Setup reset-এর sample members আর live sequence-assigned roll/reg আলাদা। Roll/reg uniqueness independent: একটি member-এর roll অন্য member-এর registration string-এর সমান হওয়া দুই-column cross-uniqueness দিয়ে আটকানো হয়নি। দুই roll কখনো এক নয় এবং দুই registration কখনো এক নয়।

Security error parsing output-এর মধ্যে ORA-/SP2- substring খোঁজে; user text-এ error-looking substring থাকলে false error classification সম্ভব। Delimiter/null-marker transport application convention; generic full-Unicode JSON database driver নয়। Main long SQL strings, repeated membership rules এবং identity-only compatibility endpoint future refactor candidates। Documentation এগুলো implementation facts হিসেবে বলে; এই task-এ application behavior বদলানো হয়নি।
""",
}

FIELDS = {
    "/api/students": "GET: নেই; POST: name,department,phone,email,roll_no,registration_no",
    "/api/students/{student_id}/edit": "name,department,phone,email,roll_no,registration_no,membership_status",
    "/api/students/{student_id}/identity": "roll_no,registration_no",
    "/api/books": "GET q optional; POST title,author,category,quantity,publisher optional",
    "/api/books/{book_id}/reduce": "quantity",
    "/api/issues": "POST studentId,bookId; GET নেই",
    "/api/audit": "q,entity,action,page query parameters",
    "/api/auth/login": "username,password",
    "/api/accounts/librarians": "username,password",
    "/api/auth/change-credentials": "currentPassword,newUsername,newPassword",
}


def write(name, content):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def purpose(relative):
    if relative in PURPOSES:
        return PURPOSES[relative]
    if relative.startswith("tests/"):
        return "Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।"
    if relative.endswith(".html"):
        return "এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।"
    return "Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।"


def explain(line, language, scope):
    text = line.strip()
    context = f" `{scope}` অংশে" if scope else ""
    if not text:
        return "খালি line; logical blocks আলাদা করে।"
    if text.startswith(("#", "//", "--", "/*", "* ", "<!--")):
        return "Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না।"
    if language == "python":
        if text.startswith(("import ", "from ")):
            return "Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে।"
        if text.startswith("@"):
            return "Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে।"
        if re.match(r"(?:async )?def ", text):
            return "Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়।"
        if text.startswith("class "):
            return "Class definition; related test/helper behavior একত্র করে।"
        if "raise " in text:
            return (
                "Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়।"
                + context
            )
        if text.startswith("return "):
            return "Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে।" + context
        if text.startswith(("if ", "elif ", "else:")):
            return "Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে।" + context
        if text.startswith(("for ", "while ")):
            return (
                "একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে।"
                + context
            )
        if text.startswith(("try:", "except ", "finally:")):
            return "Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block।" + context
        if "assert" in text or "self.assert" in text:
            return "Expected behavior/values পরীক্ষা করে; mismatch test failure করে।"
        if "await " in text:
            return "Asynchronous operation-এর result-এর জন্য অপেক্ষা করে।" + context
        if "run_sql(" in text or "execute_dml(" in text:
            return (
                "Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়।"
                + context
            )
        if "rows(" in text:
            return "SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়।" + context
        if "=" in text:
            return (
                "Value/configuration/query/result কোনো variable অথবা object field-এ assign করে।"
                + context
            )
        return (
            "চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো।"
            + context
        )
    if language == "javascript":
        if (
            "addEventListener" in text
            or ".onclick" in text
            or ".onsubmit" in text
            or ".oninput" in text
            or ".onchange" in text
        ):
            return "User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে।"
        if "function " in text:
            return "Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়।"
        if "innerHTML" in text:
            return "Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে।"
        if "textContent" in text:
            return "Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না।"
        if "fetch(" in text or "api(" in text:
            return "HTTP/API request করে; response asynchronousভাবে process হয়।"
        if "FormData" in text or "URLSearchParams" in text:
            return (
                "Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে।"
            )
        if "escapeHtml(" in text:
            return "User/database values escaped display markup-এ রূপান্তর করে।"
        if "setAttribute" in text:
            return "DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়।"
        if "setTimeout" in text or "setInterval" in text or "clearTimeout" in text:
            return "Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে।"
        if "preventDefault" in text:
            return "Default form navigation বন্ধ করে controlled API submission চালাতে দেয়।"
        if ".filter(" in text:
            return "Search/eligibility/status condition মেলে এমন records নির্বাচন করে।"
        if ".map(" in text:
            return "প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে।"
        if "return " in text:
            return "Current callback/function result ফেরায় অথবা branch early-exit করে।"
        if "catch" in text or "finally" in text or "try" in text:
            return "Async failure handling ও UI cleanup/restore block।"
        if "if " in text or " ? " in text:
            return "Condition অনুযায়ী action/label/value নির্বাচন করে।"
        if "=" in text:
            return "Local state, DOM reference বা callback/result assign করে।"
        return (
            "Expression/template literal বা enclosing callback/function-এর structural continuation।"
        )
    if language == "html":
        tags = re.findall(r"<([a-zA-Z][\w-]*)", text)
        descriptions = {
            "input": "user-entered field; name request key, required/pattern/maxlength browser validation",
            "label": "field-এর readable label",
            "button": "action/submit/cancel control",
            "select": "option থেকে value নির্বাচন",
            "option": "select-এর choice",
            "script": "JavaScript controller load",
            "link": "stylesheet/resource load",
            "section": "related UI content grouping",
            "form": "submit-able input grouping",
            "main": "primary page content",
            "div": "layout/dynamic content container",
            "meta": "encoding/viewport metadata",
            "h1": "page heading",
            "h2": "section/dialog heading",
            "p": "description/help text",
            "footer": "developer credit/footer",
            "progress": "quantity ratio indicator",
        }
        return (
            "; ".join(
                f"{tag}: {descriptions.get(tag, 'HTML structure/content')}"
                for tag in dict.fromkeys(tags)
            )
            or "HTML closing structure অথবা text content; আগের open elements-এর অংশ।"
        )
    if language == "css":
        if "@media" in text:
            return "Viewport condition অনুযায়ী responsive styles apply করে।"
        if "@supports" in text:
            return "Browser feature support অনুযায়ী fallback style নির্বাচন করে।"
        if text.startswith("--"):
            return "Reusable CSS custom property/design token define করে।"
        if "{" in text:
            return "Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে।"
        props = re.findall(r"([\w-]+)\s*:", text)
        return (
            "CSS properties: "
            + ", ".join(props)
            + "; enclosing selector-এর presentation নির্ধারণ করে।"
            if props
            else "Style rule/block-এর closing বা continuation।"
        )
    if language == "sql":
        upper = text.upper()
        if "CREATE " in upper:
            return "Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger।"
        if "ALTER " in upper:
            return "Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে।"
        if upper.startswith("SET "):
            return "SQL*Plus client output/substitution configuration; database business row update নয়।"
        if upper.startswith("WHENEVER "):
            return (
                "SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে।"
            )
        if text.startswith("@@"):
            return "Current SQL script-এর directory থেকে referenced feature script চালায়।"
        if "SELECT " in upper:
            return "Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে।"
        if "INSERT " in upper:
            return "নতুন business/audit/sample row insert করার statement।"
        if "UPDATE " in upper and not upper.startswith("AFTER"):
            return "Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে।"
        if "FOR UPDATE" in upper or "LOCK TABLE" in upper:
            return "Concurrent changes নিয়ন্ত্রণে database lock নেয়।"
        if "RAISE" in upper:
            return "Database business validation অথবা setup verification fail হলে Oracle exception তোলে।"
        if "EXCEPTION" in upper:
            return "PL/SQL error branch; known conflict/no-data conditions handle করে।"
        if "COMMIT" in upper:
            return (
                "Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ।"
            )
        if "ROLLBACK" in upper:
            return "Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না।"
        if upper.startswith(("IF ", "ELSIF ", "ELSE", "END IF")):
            return "PL/SQL condition/alternative branch।"
        if "PRIMARY KEY" in upper or "REFERENCES" in upper or "CHECK" in upper or "UNIQUE" in upper:
            return (
                "Schema integrity rule: record identity, foreign key, domain বা uniqueness checks।"
            )
        if "AUDIT_JSON_VALUE" in upper:
            return "Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে।"
        if "NEXTVAL" in upper:
            return "Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না।"
        if text == "/":
            return "SQL*Plus আগের PL/SQL buffer execute করার delimiter।"
        if upper.startswith("PROMPT"):
            return "Script progress/completion message output করে।"
        return "PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো।"
    return "Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়।"


def python_functions(source):
    tree = ast.parse(source)
    nodes = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return sorted(nodes, key=lambda node: node.lineno)


def sources():
    files = []
    for folder in ("backend", "frontend", "database", "tests"):
        files.extend(
            p
            for p in (ROOT / folder).rglob("*")
            if p.is_file()
            and p.suffix in {".py", ".js", ".cjs", ".html", ".css", ".sql", ".txt", ".ora"}
            and "__pycache__" not in p.parts
            and "backups" not in p.parts
        )
    for name in (
        "README.md",
        "run.ps1",
        "Open-Library-Project.bat",
        "Setup-Database.bat",
        ".env.example",
        ".gitignore",
        ".vscode/settings.json",
        "overview/tools/generate_docs.py",
    ):
        if (ROOT / name).is_file():
            files.append(ROOT / name)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def build():
    inventory = []
    api = []
    index = [
        "# প্রতিটি file-এর পূর্ণ code ও ব্যাখ্যা",
        "",
        "প্রতিটি linked guide-এ file purpose, function/object/element inventory, original source এবং প্রতিটি source line-এর reading notes আছে। Blank lines-ও reference রাখা হয়েছে। Line notes syntax reading সহায়ক; complex business semantics curated chapters ও function explanations-এ দেওয়া।",
        "",
        "| File | Lines | Guide |",
        "| --- | --- | --- |",
    ]
    languages = {
        ".py": "python",
        ".js": "javascript",
        ".cjs": "javascript",
        ".html": "html",
        ".css": "css",
        ".sql": "sql",
        ".json": "json",
        ".ps1": "powershell",
        ".bat": "bat",
    }
    for path in sources():
        relative = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        source = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        lines = source.splitlines()
        language = languages.get(path.suffix, "text")
        guide = "code/" + relative.replace("/", "__") + ".md"
        inventory.append(
            {
                "path": relative,
                "lines": len(lines),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "guide": guide,
            }
        )
        index.append(f"| `{relative}` | {len(lines)} | [বিস্তারিত]({guide}) |")
        body = [
            f"# {relative}",
            "",
            purpose(relative),
            "",
            f"Source: [মূল file]({'../' * 2}{relative})। Snapshot {DATE}; {len(lines)} lines; SHA-256 `{inventory[-1]['sha256']}`।",
            "",
            "## Function / object / element inventory",
            "",
        ]
        functions = []
        if language == "python":
            functions = python_functions(source)
            for node in functions:
                signature = lines[node.lineno - 1].strip()
                description = FUNCTIONS.get(
                    node.name,
                    "Test/setup helper: "
                    + node.name.replace("_", " ")
                    + "; নিচের assertions/calls সেই behavior define করে।",
                )
                body += [
                    f"### `{node.name}` — L{node.lineno}–L{node.end_lineno}",
                    "",
                    f"`{signature}`",
                    "",
                    description,
                    "",
                ]
                for decorator in node.decorator_list:
                    if (
                        relative.startswith("backend/")
                        and isinstance(decorator, ast.Call)
                        and isinstance(decorator.func, ast.Attribute)
                        and decorator.func.attr in {"get", "post", "delete", "put", "patch"}
                        and decorator.args
                        and isinstance(decorator.args[0], ast.Constant)
                    ):
                        route = decorator.args[0].value
                        admin = (
                            "ADMIN"
                            if node.name
                            in {
                                "get_accounts",
                                "create_librarian",
                                "toggle_librarian",
                                "delete_librarian",
                                "change_admin_credentials",
                                "audit_page",
                                "get_audit",
                                "accounts_page",
                            }
                            else (
                                "Public/session-specific"
                                if route
                                in {
                                    "/login",
                                    "/api/health",
                                    "/api/auth/login",
                                    "/api/auth/session",
                                    "/api/auth/logout",
                                }
                                else "ADMIN/LIBRARIAN session"
                            )
                        )
                        method = decorator.func.attr.upper()
                        fields = FIELDS.get(route, "Path ID যেখানে আছে; অতিরিক্ত form field নেই")
                        if method == "GET" and route in {"/api/students", "/api/issues"}:
                            fields = "Form/query fields নেই"
                        elif method == "GET" and route == "/api/books":
                            fields = "q optional query parameter"
                        elif method == "POST" and route == "/api/books":
                            fields = "title,author,category,quantity; publisher optional"
                        elif method == "POST" and route == "/api/students":
                            fields = "name,department,phone,email,roll_no,registration_no"
                        elif method == "POST" and route == "/api/issues":
                            fields = "studentId,bookId"
                        api.append(
                            (
                                method,
                                route,
                                node.name,
                                admin,
                                fields,
                                relative,
                                node.lineno,
                                description,
                            )
                        )
        elif language == "javascript":
            for match in re.finditer(r"(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)", source):
                name = match.group(1)
                line = source[: match.start()].count("\n") + 1
                body += [
                    f"### `{name}({match.group(2)})` — L{line}",
                    "",
                    FUNCTIONS.get(
                        name, "Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।"
                    ),
                    "",
                ]
            if relative.endswith("login.js"):
                body += [
                    "Login controller named functions-এর বদলে onclick/onsubmit callbacks ব্যবহার করে। submitting guard, AbortController, JSON/role response check, error message ও finally cleanup প্রতিটি branch নিচে আছে।",
                    "",
                ]
        elif language == "sql":
            objects = re.findall(
                r"CREATE\s+(?:OR REPLACE\s+)?(?:UNIQUE\s+)?(TABLE|SEQUENCE|TRIGGER|PROCEDURE|FUNCTION|VIEW|INDEX)\s+(\w+)",
                source,
                re.I,
            )
            for kind, name in objects:
                description = (
                    "প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।"
                    if name.startswith("audit_") and kind.upper() == "TRIGGER"
                    else (
                        "Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।"
                        if kind.upper() == "SEQUENCE"
                        else (
                            "Database integrity/search performance enforce করে।"
                            if kind.upper() == "INDEX"
                            else "উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।"
                        )
                    )
                )
                body += [f"- **{kind.upper()} `{name}`**: {description}"]
            body += [""]
        elif language == "html":
            ids = re.findall(r'\bid="([^"]+)"', source)
            fields = re.findall(r'<(?:input|select)[^>]*\bname="([^"]+)"', source)
            resources = re.findall(r'(?:src|href)="([^"]+)"', source)
            body += [
                "- DOM IDs: " + ", ".join(f"`{v}`" for v in ids),
                "- Form keys: " + ", ".join(f"`{v}`" for v in fields),
                "- Loaded/linked resources: " + ", ".join(f"`{v}`" for v in resources),
                "",
            ]
        elif language == "css":
            body += [
                "CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।",
                "",
            ]
        runs = re.findall(r"`+", source)
        fence = "`" * max(3, 1 + max((len(run) for run in runs), default=0))
        body += [
            "## সম্পূর্ণ original source",
            "",
            fence + language,
            source.rstrip("\n"),
            fence,
            "",
            "## প্রতিটি line-এর reading notes",
            "",
            "| Line | Original line | ব্যাখ্যা |",
            "| --- | --- | --- |",
        ]
        for number, line in enumerate(lines, 1):
            scopes = [node for node in functions if node.lineno <= number <= node.end_lineno]
            scope = (
                min(scopes, key=lambda node: node.end_lineno - node.lineno).name if scopes else ""
            )
            escaped = html.escape(line).replace("|", "&#124;")
            note = explain(line, language, scope).replace("|", "&#124;")
            body.append(f"| {number} | <code>{escaped or '&nbsp;'}</code> | {note} |")
        write(guide, "\n".join(body))
    write("11-file-code-index.md", "\n".join(index))
    api_content = [
        "# API ও page endpoint reference",
        "",
        "শুধু backend-এর source decorators থেকে extracted; router nested functions-ও included। Test-only /api/private বা fake test health production route নয়। Form bodies URL-encoded, audit/search parameters query string। API responses JSON; page responses HTML।",
        "",
        "StaticFiles mount `GET /static/{path}`-এ frontend assets দেয়; এটি decorator route নয়। New book/member/issue/librarian creation routes success-এ 201; অন্য JSON routes default 200। Page redirects 303; errors নিচের backend guide-এ দেওয়া।",
        "",
        "| Method | Path | Handler | Permission | Inputs |",
        "| --- | --- | --- | --- | --- |",
    ]
    for method, route, name, role, fields, relative, line, description in sorted(api):
        api_content.append(
            f"| {method} | `{route}` | [{name}](../{relative}#L{line}) | {role} | {fields} |"
        )
    for method, route, name, role, fields, relative, line, description in sorted(api):
        api_content += [
            "",
            f"## {method} {route}",
            "",
            description,
            "",
            f"Handler `{name}`; source `{relative}:{line}`। Inputs: {fields}। Permission: {role}।",
        ]
    write("12-api-reference.md", "\n".join(api_content))
    for filename, text in CHAPTERS.items():
        write(filename, text)
    assets = [p for p in (ROOT / "frontend/assets").glob("*") if p.is_file()]
    asset_text = [
        "# Images ও non-source files",
        "",
        "Images binary visual assets, executable code নয়; original image file link এবং SHA-256 দিয়ে exact artifact শনাক্ত করা যায়।",
        "",
        "| Asset | Bytes | SHA-256 | ব্যবহার |",
        "| --- | --- | --- | --- |",
    ]
    for path in assets:
        rel = path.relative_to(ROOT).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        use = (
            "Login campus background"
            if path.name == "pstu-library.jpg"
            else "Dashboard cover ও login fallback"
        )
        asset_text.append(
            f"| [{path.name}](../{rel}) | {path.stat().st_size} | `{digest}` | {use} |"
        )
        inventory.append(
            {"path": rel, "bytes": path.stat().st_size, "sha256": digest, "type": "binary asset"}
        )
    asset_text += [
        "",
        "## Runtime/local files",
        "",
        "- `.env`: real database credentials; contents intentionally excluded. Configuration semantics ও .env.example guide দেখো।",
        "- `sqlnet.log`/`*.log`: runtime diagnostic output; source নয়, connection errors থাকতে পারে।",
        "- `__pycache__`/`*.pyc`: interpreter-generated bytecode; source Python guides authoritative।",
        "- Documentation live member records/passwords export করে না। Source seed/sample values full SQL guide-এ আছে।",
        "",
    ]
    write("13-assets-and-runtime-files.md", "\n".join(asset_text))
    write(
        "manifest.json",
        json.dumps(
            {
                "snapshot_date": DATE,
                "source_files": inventory,
                "private_files_excluded": [".env"],
                "generated": "Source code guides + curated chapters; app/database unchanged",
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    readme = [
        "# PSTU Library — A to Z Project Overview",
        "",
        f"Documentation snapshot: **{DATE} (Asia/Dhaka)**। বাংলায় project explanation, পূর্ণ source, function inventory, line references এবং operational guide।",
        "",
        "## পড়ার ক্রম",
        "",
    ]
    titles = [
        ("01-project-and-architecture.md", "Project ও architecture"),
        ("02-setup-and-configuration.md", "Setup ও configuration"),
        ("03-backend-and-validation.md", "Backend ও validation"),
        ("04-authentication-and-security.md", "Authentication ও security"),
        ("05-database-and-business-rules.md", "Database ও business rules"),
        ("06-frontend-and-design.md", "Frontend ও design"),
        ("07-audit-and-transactions.md", "Audit ও transactions"),
        ("08-operation-walkthroughs.md", "End-to-end workflows"),
        ("09-testing-and-maintenance.md", "Tests ও maintenance"),
        ("10-troubleshooting-and-limitations.md", "Troubleshooting ও limitations"),
        ("11-file-code-index.md", "প্রতিটি file-এর পূর্ণ code ও line-by-line guide"),
        ("12-api-reference.md", "সব endpoints-এর reference"),
        ("13-assets-and-runtime-files.md", "Images, runtime files ও exclusions"),
        ("14-data-dictionary-and-responses.md", "প্রতিটি database field ও response schema"),
        ("15-code-concepts-and-dependencies.md", "Code concepts ও dependencies glossary"),
    ]
    readme += [f"{i}. [{title}]({filename})" for i, (filename, title) in enumerate(titles, 1)]
    readme += [
        "",
        "## Coverage ও refresh",
        "",
        f"{len([item for item in inventory if 'guide' in item])}টি text/source/configuration file-এর পূর্ণ code ও প্রতিটি line-এর reading notes; {len(assets)}টি image asset-এর inventory। API documentation source decorators থেকে তৈরি। manifest.json-এ paths/line counts/SHA-256 আছে।",
        "",
        "Private .env credentials, generated caches/logs ও historical local backups-এর full contents included নয়; তাদের ভূমিকা document করা হয়েছে। কোনো live personal data dump নেই। Public sample SQL অপরিবর্তিতভাবে code guide-এ আছে।",
        "",
        "Refresh: `python 'Important files/overview/tools/generate_docs.py'`। Current source snapshot বদলালে docs regenerate করো এবং curated narrative review করো। [Generator পূর্ণ code](code/overview__tools__generate_docs.py.md)।",
        "",
        "Application behavior অথবা database records এই documentation task-এ পরিবর্তন করা হয়নি। Source guide-এর syntax notes ও curated business explanation একসঙ্গে পড়লে code বুঝতে সুবিধা হবে।",
    ]
    readme.extend(
        [
            "",
            "## SQL references",
            "",
            "- [Output দেখার queries ও backend SQL templates](queries.md)",
            "- [Database-এর সম্পূর্ণ SQL code](database-full-code.md)",
            "",
            "এই দুই reference update করতে `python 'Important files/overview/tools/export_sql_reference.py'` চালান।",
        ]
    )
    write("README.md", "\n".join(readme))
    print(
        f"Generated {len(inventory)} inventory entries, {len(api)} routes and {len(CHAPTERS)} chapters in {OUT}"
    )


PURPOSES["frontend/fines.js"] = (
    "Overdue loans, Oracle-calculated daily fine estimates, Return book actions, return/payment history and combined outstanding totals; paid fines excluded and issues never counted twice."
)
FUNCTIONS[
    "get_issues"
] += " The response also includes numeric overdue_days and current_fine, calculated from Oracle TRUNC(SYSDATE) using the same Tk 10/day rule as return_book_proc; returned loans return zero estimates."
FUNCTIONS["memberCell"] = (
    "Render internal member ID, name, academic roll and registration for a fine/overdue row."
)
FUNCTIONS["performAction"] = (
    "Confirm and execute one return/payment POST, disable its button while pending, reload live data and restore the button on completion."
)

FUNCTIONS["get_snapshot"] = (
    "Collect the existing books/member/loan/fine/metadata SELECT definitions and execute all seven in one Oracle connection; return one complete management dataset."
)
FUNCTIONS["collect_reads"] = (
    "Request-context-scoped query collector; rows records definitions without SQL execution, then resets the context in finally."
)
FUNCTIONS["read_many"] = (
    "Validate read-only SELECTs, add section markers, run one SQLPlus session, verify complete ordered output and decode each result."
)
FUNCTIONS["parse_rows"] = (
    "Decode pipe-delimited output, null markers and typed numeric fields; reject malformed rows."
)
FUNCTIONS["loadData"] = (
    "Coalesce overlapping requests and GET /api/snapshot instead of five separate read endpoints; update live state and connection status together."
)

PURPOSES.update(
    {
        "backend/main.py": "Create the app, register authentication and feature routers, and serve static files.",
        "backend/routes/pages.py": "Serve management pages and report Oracle connectivity.",
        "backend/routes/books.py": "Read the catalogue and manage physical copies and stock.",
        "backend/routes/members.py": "Create and edit library members and their membership status.",
        "backend/routes/circulation.py": "Issue and return physical book copies.",
        "backend/routes/fines.py": "Read fines, accept full-balance payments and list receipts.",
        "backend/routes/snapshot.py": "Collect the complete management dataset in one Oracle connection.",
        "backend/routes/audit.py": "Administrator audit search, filters and pagination.",
        "backend/auth/member_access.py": "Member-only self activation and verified password recovery.",
        "backend/auth/validation.py": "Validate member IDs, staff usernames and account passwords.",
        "frontend/member-dashboard.js": "Render personal borrowing, reservations, catalogue, fines and security controls.",
        "frontend/reservation-desk.js": "Render staff reservation controls and available member/book choices.",
        "frontend/reservations.js": "Coordinate page-specific views, refresh requests and reservation actions.",
        "database/setup.sql": "Run fresh-install schema modules, upgrades, sample records and verification in dependency order.",
    }
)

if __name__ == "__main__":
    build()
