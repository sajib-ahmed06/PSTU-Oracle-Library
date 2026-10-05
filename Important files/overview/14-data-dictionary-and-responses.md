# প্রতিটি database field ও API response

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
