# API ও page endpoint reference

শুধু backend-এর source decorators থেকে extracted; router nested functions-ও included। Test-only /api/private বা fake test health production route নয়। Form bodies URL-encoded, audit/search parameters query string। API responses JSON; page responses HTML।

StaticFiles mount `GET /static/{path}`-এ frontend assets দেয়; এটি decorator route নয়। New book/member/issue/librarian creation routes success-এ 201; অন্য JSON routes default 200। Page redirects 303; errors নিচের backend guide-এ দেওয়া।

| Method | Path | Handler | Permission | Inputs |
| --- | --- | --- | --- | --- |
| DELETE | `/api/accounts/{user_id}` | [delete_librarian](../backend/auth/routes.py#L160) | ADMIN | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/` | [home](../backend/routes/pages.py#L15) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/accounts` | [accounts_page](../backend/routes/pages.py#L40) | ADMIN | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/activate-account` | [activation_page](../backend/auth/member_access.py#L73) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/accounts` | [get_accounts](../backend/auth/routes.py#L121) | ADMIN | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/audit` | [get_audit](../backend/routes/audit.py#L14) | ADMIN | q,entity,action,page query parameters |
| GET | `/api/auth/session` | [auth_session](../backend/auth/routes.py#L104) | Public/session-specific | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/books` | [get_books](../backend/routes/books.py#L12) | ADMIN/LIBRARIAN session | q optional query parameter |
| GET | `/api/books/{book_id}/copies` | [get_book_copies](../backend/routes/books.py#L95) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/fines` | [get_fines](../backend/routes/fines.py#L30) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/fines/collection-summary` | [get_collection_summary](../backend/routes/fines.py#L14) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/fines/{fine_id}/payments` | [get_fine_payments](../backend/routes/fines.py#L70) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/health` | [health](../backend/routes/pages.py#L47) | Public/session-specific | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/issues` | [get_issues](../backend/routes/circulation.py#L12) | ADMIN/LIBRARIAN session | Form/query fields নেই |
| GET | `/api/meta` | [get_meta](../backend/routes/snapshot.py#L15) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/reservations` | [get_reservations](../backend/reservations.py#L110) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/snapshot` | [get_snapshot](../backend/routes/snapshot.py#L30) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/student/dashboard` | [student_dashboard](../backend/reservations.py#L75) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/api/students` | [get_students](../backend/routes/members.py#L18) | ADMIN/LIBRARIAN session | Form/query fields নেই |
| GET | `/audit` | [audit_page](../backend/routes/pages.py#L53) | ADMIN | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/books` | [books_page](../backend/routes/pages.py#L20) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/circulation` | [circulation_page](../backend/routes/pages.py#L30) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/fines` | [fines_page](../backend/routes/pages.py#L35) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/forgot-password` | [recovery_page](../backend/auth/member_access.py#L17) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/login` | [login_page](../backend/auth/routes.py#L30) | Public/session-specific | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/reservations` | [reservations_page](../backend/reservations.py#L70) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/student` | [student_page](../backend/reservations.py#L66) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| GET | `/students` | [students_page](../backend/routes/pages.py#L25) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/accounts/librarians` | [create_librarian](../backend/auth/routes.py#L132) | ADMIN | username,password |
| POST | `/api/accounts/{user_id}/toggle` | [toggle_librarian](../backend/auth/routes.py#L148) | ADMIN | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/auth/activate` | [activate](../backend/auth/member_access.py#L77) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/auth/change-credentials` | [change_admin_credentials](../backend/auth/routes.py#L168) | ADMIN | currentPassword,newUsername,newPassword |
| POST | `/api/auth/login` | [login](../backend/auth/routes.py#L36) | Public/session-specific | username,password |
| POST | `/api/auth/logout` | [logout](../backend/auth/routes.py#L114) | Public/session-specific | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/auth/reset-password` | [reset_password](../backend/auth/member_access.py#L21) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/books` | [add_book](../backend/routes/books.py#L35) | ADMIN/LIBRARIAN session | title,author,category,quantity; publisher optional |
| POST | `/api/books/{book_id}/reduce` | [reduce_book_stock](../backend/routes/books.py#L110) | ADMIN/LIBRARIAN session | quantity |
| POST | `/api/fines/{fine_id}/pay` | [pay_fine](../backend/routes/fines.py#L55) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/issues` | [add_issue](../backend/routes/circulation.py#L44) | ADMIN/LIBRARIAN session | studentId,bookId |
| POST | `/api/issues/{issue_id}/return` | [return_book](../backend/routes/circulation.py#L66) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/reservations` | [reserve](../backend/reservations.py#L117) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/reservations/{reservation_id}/cancel` | [cancel](../backend/reservations.py#L160) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/reservations/{reservation_id}/collect` | [collect](../backend/reservations.py#L164) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/student/password` | [student_password](../backend/reservations.py#L168) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |
| POST | `/api/students` | [add_student](../backend/routes/members.py#L41) | ADMIN/LIBRARIAN session | name,department,phone,email,roll_no,registration_no |
| POST | `/api/students/{student_id}/edit` | [edit_student](../backend/routes/members.py#L72) | ADMIN/LIBRARIAN session | name,department,phone,email,roll_no,registration_no,membership_status |
| POST | `/api/students/{student_id}/identity` | [update_student_identity](../backend/routes/members.py#L117) | ADMIN/LIBRARIAN session | roll_no,registration_no |
| POST | `/api/students/{student_id}/toggle` | [toggle_student_membership](../backend/routes/members.py#L139) | ADMIN/LIBRARIAN session | Path ID যেখানে আছে; অতিরিক্ত form field নেই |

## DELETE /api/accounts/{user_id}

Admin-only librarian যাচাই করে delete করে এবং তার sessions invalidates করে। Admin account এই helper দিয়ে delete হয় না।

Handler `delete_librarian`; source `backend/auth/routes.py:160`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN।

## GET /

Dashboard index.html response দেয়; authentication middleware আগেই access check করে।

Handler `home`; source `backend/routes/pages.py:15`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /accounts

ADMIN role ছাড়া dashboard redirect দেয়; admin হলে accounts.html দেয়।

Handler `accounts_page`; source `backend/routes/pages.py:40`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN।

## GET /activate-account

Test/setup helper: activation page; নিচের assertions/calls সেই behavior define করে।

Handler `activation_page`; source `backend/auth/member_access.py:73`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/accounts

Admin permission যাচাই করে admin/librarian account metadata ফেরায়; passwords select করে না।

Handler `get_accounts`; source `backend/auth/routes.py:121`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN।

## GET /api/audit

Admin-only search/entity/action filters ও 25-row Oracle ROWNUM pagination; RAWTOHEX snapshots decode করে JSON before/after ফেরায়। Stored UTC timestamps UI-তে Dhaka সময় হয়।

Handler `get_audit`; source `backend/routes/audit.py:14`। Inputs: q,entity,action,page query parameters। Permission: ADMIN।

## GET /api/auth/session

Current session থেকে username ও user_type JSON দেয়; session না থাকলে 401।

Handler `auth_session`; source `backend/auth/routes.py:104`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: Public/session-specific।

## GET /api/books

book_details view থেকে title/author/category search ও available/total stock ফেরায়। Search SQL LIKE হওয়ায় % ও _ wildcard হতে পারে।

Handler `get_books`; source `backend/routes/books.py:12`। Inputs: q optional query parameter। Permission: ADMIN/LIBRARIAN session।

## GET /api/books/{book_id}/copies

Test/setup helper: get book copies; নিচের assertions/calls সেই behavior define করে।

Handler `get_book_copies`; source `backend/routes/books.py:95`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/fines

Fine, issue, student ও book join করে amount ও payment status দেখায়।

Handler `get_fines`; source `backend/routes/fines.py:30`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/fines/collection-summary

Test/setup helper: get collection summary; নিচের assertions/calls সেই behavior define করে।

Handler `get_collection_summary`; source `backend/routes/fines.py:14`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/fines/{fine_id}/payments

Test/setup helper: get fine payments; নিচের assertions/calls সেই behavior define করে।

Handler `get_fine_payments`; source `backend/routes/fines.py:70`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/health

dual-এ SELECT 1 চালিয়ে actual Oracle connectivity যাচাই করে CONNECTED metadata দেয়। এটি public endpoint।

Handler `health`; source `backend/routes/pages.py:47`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: Public/session-specific।

## GET /api/issues

Loan, student ও book join করে issue/due/return dates এবং status JSON rows দেয়; newest issue আগে। The response also includes numeric overdue_days and current_fine, calculated from Oracle TRUNC(SYSDATE) using the same Tk 10/day rule as return_book_proc; returned loans return zero estimates.

Handler `get_issues`; source `backend/routes/circulation.py:12`। Inputs: Form/query fields নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/meta

Author/category IDs ও names দেয়; book form datalist-এর options হিসেবে ব্যবহৃত।

Handler `get_meta`; source `backend/routes/snapshot.py:15`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/reservations

Test/setup helper: get reservations; নিচের assertions/calls সেই behavior define করে।

Handler `get_reservations`; source `backend/reservations.py:110`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/snapshot

Collect the existing books/member/loan/fine/metadata SELECT definitions and execute all seven in one Oracle connection; return one complete management dataset.

Handler `get_snapshot`; source `backend/routes/snapshot.py:30`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/student/dashboard

Test/setup helper: student dashboard; নিচের assertions/calls সেই behavior define করে।

Handler `student_dashboard`; source `backend/reservations.py:75`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /api/students

Member directory ফেরায়; generated student_id, contact/status এবং separate roll_no/registration_no fields থাকে।

Handler `get_students`; source `backend/routes/members.py:18`। Inputs: Form/query fields নেই। Permission: ADMIN/LIBRARIAN session।

## GET /audit

Admin permission ছাড়া access reject করে; admin-কে audit.html response দেয়।

Handler `audit_page`; source `backend/routes/pages.py:53`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN।

## GET /books

Books page HTML পরিবেশন করে।

Handler `books_page`; source `backend/routes/pages.py:20`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /circulation

Issue/Return page HTML পরিবেশন করে।

Handler `circulation_page`; source `backend/routes/pages.py:30`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /fines

Fine register HTML পরিবেশন করে।

Handler `fines_page`; source `backend/routes/pages.py:35`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /forgot-password

Test/setup helper: recovery page; নিচের assertions/calls সেই behavior define করে।

Handler `recovery_page`; source `backend/auth/member_access.py:17`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /login

Session থাকলে dashboard redirect; না থাকলে login.html FileResponse দেয়।

Handler `login_page`; source `backend/auth/routes.py:30`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: Public/session-specific।

## GET /reservations

Test/setup helper: reservations page; নিচের assertions/calls সেই behavior define করে।

Handler `reservations_page`; source `backend/reservations.py:70`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /student

Test/setup helper: student page; নিচের assertions/calls সেই behavior define করে।

Handler `student_page`; source `backend/reservations.py:66`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## GET /students

Members directory HTML পরিবেশন করে।

Handler `students_page`; source `backend/routes/pages.py:25`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/accounts/librarians

Admin-only username/password validation, duplicate check ও hashed password insertion করে; role LIBRARIAN এবং status ACTIVE।

Handler `create_librarian`; source `backend/auth/routes.py:132`। Inputs: username,password। Permission: ADMIN।

## POST /api/accounts/{user_id}/toggle

Admin-only target librarian status পরিবর্তন করে; disabled হলে তার active sessions সরিয়ে দেয়।

Handler `toggle_librarian`; source `backend/auth/routes.py:148`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN।

## POST /api/auth/activate

Test/setup helper: activate; নিচের assertions/calls সেই behavior define করে।

Handler `activate`; source `backend/auth/member_access.py:77`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/auth/change-credentials

Current password verify করে নতুন username/password validate ও update করে; অন্য sessions বাতিল করে current token-এর session ধরে রাখে।

Handler `change_admin_credentials`; source `backend/auth/routes.py:168`। Inputs: currentPassword,newUsername,newPassword। Permission: ADMIN।

## POST /api/auth/login

Form parse ও length check করে authenticate helper worker thread-এ চালায়; পুরোনো cookie session সরিয়ে নতুন HttpOnly SameSite=strict cookie দেয়। HTTPS হলে Secure flag।

Handler `login`; source `backend/auth/routes.py:36`। Inputs: username,password। Permission: Public/session-specific।

## POST /api/auth/logout

Cookie token invalidates করে browser cookie delete response দেয়।

Handler `logout`; source `backend/auth/routes.py:114`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: Public/session-specific।

## POST /api/auth/reset-password

Test/setup helper: reset password; নিচের assertions/calls সেই behavior define করে।

Handler `reset_password`; source `backend/auth/member_access.py:21`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/books

Form validate করে author/category resolve বা create করে; matching book row lock করে restock, নয়তো নতুন title insert; transaction শেষে commit।

Handler `add_book`; source `backend/routes/books.py:35`। Inputs: title,author,category,quantity; publisher optional। Permission: ADMIN/LIBRARIAN session।

## POST /api/books/{book_id}/reduce

Book lock করে requested quantity available stock ছাড়িয়েছে কি না দেখে; total ও available উভয় count কমায়। Borrowed copies বাদ দেওয়া যায় না।

Handler `reduce_book_stock`; source `backend/routes/books.py:110`। Inputs: quantity। Permission: ADMIN/LIBRARIAN session।

## POST /api/fines/{fine_id}/pay

Target fine PAID update করে; affected row না থাকলে NO_DATA_FOUND; audit trigger-সহ commit করে। Already-paid row আবার update করলেও নতুন audit event হতে পারে।

Handler `pay_fine`; source `backend/routes/fines.py:55`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/issues

Student ও book IDs positive integer যাচাই করে issue_book_proc call এবং commit করে।

Handler `add_issue`; source `backend/routes/circulation.py:44`। Inputs: studentId,bookId। Permission: ADMIN/LIBRARIAN session।

## POST /api/issues/{issue_id}/return

Positive issue ID নিয়ে return_book_proc call করে; returned inventory/fine changes এক transaction-এ commit।

Handler `return_book`; source `backend/routes/circulation.py:66`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/reservations

Test/setup helper: reserve; নিচের assertions/calls সেই behavior define করে।

Handler `reserve`; source `backend/reservations.py:117`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/reservations/{reservation_id}/cancel

Test/setup helper: cancel; নিচের assertions/calls সেই behavior define করে।

Handler `cancel`; source `backend/reservations.py:160`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/reservations/{reservation_id}/collect

Test/setup helper: collect; নিচের assertions/calls সেই behavior define করে।

Handler `collect`; source `backend/reservations.py:164`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/student/password

Test/setup helper: student password; নিচের assertions/calls সেই behavior define করে।

Handler `student_password`; source `backend/reservations.py:168`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।

## POST /api/students

Shared member validation ও existing phone check করে সাত argument-সহ add_student_proc চালায়; identity trigger ও unique indexes final integrity enforce করে।

Handler `add_student`; source `backend/routes/members.py:41`। Inputs: name,department,phone,email,roll_no,registration_no। Permission: ADMIN/LIBRARIAN session।

## POST /api/students/{student_id}/edit

পুরো member details ও membership_status validate করে; target row lock করে disabling-এর loan/fine restrictions checks; সব editable fields এক transaction-এ update করে।

Handler `edit_student`; source `backend/routes/members.py:72`। Inputs: name,department,phone,email,roll_no,registration_no,membership_status। Permission: ADMIN/LIBRARIAN session।

## POST /api/students/{student_id}/identity

Compatibility endpoint: শুধু roll ও registration update করে; missing row-তে 404 mapping-এর জন্য NO_DATA_FOUND তোলে। Current UI full edit endpoint ব্যবহার করে।

Handler `update_student_identity`; source `backend/routes/members.py:117`। Inputs: roll_no,registration_no। Permission: ADMIN/LIBRARIAN session।

## POST /api/students/{student_id}/toggle

Member lock করে ACTIVE থেকে DISABLED যাওয়ার আগে active loans/unpaid fines দেখে; DISABLED হলে ACTIVE করে।

Handler `toggle_student_membership`; source `backend/routes/members.py:139`। Inputs: Path ID যেখানে আছে; অতিরিক্ত form field নেই। Permission: ADMIN/LIBRARIAN session।
