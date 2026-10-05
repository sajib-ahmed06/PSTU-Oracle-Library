# README.md

Project চালানো, database upgrade, structure, login flow, member identifiers ও audit সম্পর্কে মূল usage guide।

Source: [মূল file](../../README.md)। Snapshot 2026-10-04; 126 lines; SHA-256 `6fbe2976b95bd64017970d68e176aee05d03adb9277cd86baa974252f0a9a5e0`।

## Function / object / element inventory

## সম্পূর্ণ original source

```text
# PSTU Central Library

FastAPI and vanilla HTML/CSS/JavaScript library management application backed by Oracle XE 10g.

## Run

Install Python dependencies with `python -m pip install -r backend/requirements.txt`.
Copy `.env.example` to `.env` and set your Oracle credentials. Environment variables override `.env`.
Oracle SQL*Plus defaults to `C:\oraclexe\app\oracle\product\10.2.0\server`; set `ORACLE_HOME` to override it.
Run `powershell -ExecutionPolicy Bypass -File run.ps1`, then open http://localhost:8091.

## Database

New loans are due **15 days after their issue date**, including reserved-copy pickups. Existing loans retain their recorded due dates.

Circulation supports up to **3 active copies per member**, including multiple copies of one title. Select books and their physical copy numbers in the issue form; all selections are issued in one transaction. Return each loan separately. Existing stock receives copy numbers during migration; older returned loans display `Legacy copy` because their physical copy was never recorded. Attach the new numbers to the physical books to use them at the desk.

The Fines page requires full payment of the outstanding balance, with an optional payment note. Custom amounts and partial payments are rejected. Existing partial payments and receipts are preserved; the next payment clears the entire remaining balance. Outstanding fines block new loans. Overdue fines remain Tk 10/day and are finalized when the copy is returned.

For an existing installation, stop the app, run `python -m backend.upgrade_circulation`, and restart `run.ps1`. This upgrade preserves existing records and can be rerun; **do not run the reset/setup script to upgrade**. Fresh setup includes the same changes. Run rollback-only Oracle integration checks with `python -c "from backend.database import ROOT,run_sql; print(run_sql('SET SERVEROUTPUT ON\n@'+str(ROOT/'tests'/'circulation_oracle.sql')))"`.

Fresh setup uses `Setup-Database.bat` and requires typing `RESET`. It replaces project tables with the schema and sample data. Existing installations keep working until setup is explicitly run. Oracle DDL commits immediately.

For a new demo installation, run `Setup-Database.bat`. It requires typing `RESET` because it drops existing library tables. Setup prompts for your administrator username and password; no shared login credentials are shipped. Configure the private Oracle credentials in .env before setup.
Management passwords are salted PBKDF2 hashes. Existing plaintext management passwords are upgraded on successful login. Unused student/admin profile passwords in the original demo schema remain legacy fields.

## Structure

- `backend/main.py`: application wiring and feature router registration.
- `backend/routes/`: pages, catalogue, members, circulation, fines, audit and snapshot endpoints.
- `backend/database.py`: configuration, SQL*Plus execution, Oracle errors and row decoding.
- `backend/validation.py`: form and field validation.
- `backend/auth/`: sessions, account routes and password hashing.
- `database/setup.sql`: ordered fresh-install entry point; `database/schema/` holds the individual schema modules.
- `database/members_audit.sql`: audit table, indexes, function and triggers, included before sample data.
- `frontend/shared.js`: API client, live data, navigation and accessible dialogs.
- `frontend/`: page-specific markup, styles and controllers.

Database outages retain the last loaded records and block changes; reconnecting reloads live records. No demo changes are presented as persisted records.
Sessions are in memory: run one server worker; restarting the server signs users out. Dates use Asia/Dhaka. SQL*Plus uses the installed database's legacy character set; full Unicode support requires a compatible database/client configuration.

## Student dashboard and reservations

Students sign in from the same login page and open `/student`. The member dashboard includes section navigation with a selected-section indicator, a welcome banner, summary cards, upcoming returns/pickups, filters for current/returned loans and available books, a searchable book-card catalogue and separate borrowing, reservation, fines and security sections. Generated library imagery is stored locally under `frontend/assets/member-*`; prompts are recorded in `frontend/assets/member-image-prompts.md`. They see the full searchable book catalogue, their own loans, due/return dates, fines and reservation history. Student sessions cannot access management APIs or other members' records.

Students choose **Activate account** on the login page, enter their library Member ID (for example `PSTU-0001`) and registered 11-digit phone number, then set and confirm a password. Activation is one-time and requires an active membership. It creates a student account or activates an existing linked student account. It cannot reset an already activated account or re-enable a disabled account. After activation, sign in with Member ID and password; staff continue using their usernames. Students can change their password from their dashboard. **Forgot password** on the login page is available only to members: Member ID, ID/Roll, Registration No., registered phone and email must all match before a new password can be set. Recovery invalidates the member's existing sessions and cannot change Admin/Librarian passwords. The library desk no longer creates student login credentials on the Reservations page.

Admin and Librarian users have **Reservations** in the navigation and dashboard. The management overview organizes quick actions, six collection/circulation summary cards, desk priorities (overdue returns, reserved pickups and unpaid fines), recent circulation and inventory health. Shared management styling is in `frontend/polish.css`, with dashboard-specific styling in `frontend/admin.css`.

Reserving holds one available physical copy for exactly 72 hours. Other members cannot borrow that copy or remove it from stock. Available counts exclude active holds. The library desk uses **Issue reserved copy** when the member collects it; the hold becomes a normal 15-day loan. Students can cancel their own holds; staff can cancel any hold. A member may have up to three loans and active reservations together, with one active reservation per title. Disabled memberships and outstanding recorded fines block new reservations.

Oracle runs an expiry job every minute, including while the web app is stopped. Queries and circulation guards release the hold at its exact deadline even between job runs. Open reservation pages refresh each minute. Reservation changes appear in Audit. Old fine receipts and existing library records are preserved.

For an existing installation, stop the app and run `python -m backend.upgrade_circulation`, then restart it. Fresh setup includes reservations and linked demo student logins. Do not reset an existing database to upgrade. Rollback-only database tests are in `tests/recovery_oracle.sql`, `tests/activation_oracle.sql`, `tests/reservations_oracle.sql` and `tests/circulation_oracle.sql`.

## Verify

Run `python -m unittest discover -s tests -v` and `python -m compileall -q backend`.
Check JavaScript with `Get-ChildItem frontend -Filter *.js | ForEach-Object { node --check $_.FullName }`.

## Login page flow

`frontend/login.html` defines the form and accessible controls. `frontend/login.css` provides the responsive glass card, autofill contrast, and background image. Save the campus photograph as `frontend/assets/pstu-library.jpg`; until that file exists, the existing library image is used.

`frontend/login.js` sends one login request at a time, trims the username, handles timeouts and server errors, and redirects after a valid management-account response. `backend/validation.py` checks form size, encoding, duplicate fields, and required fields. `backend/auth/routes.py` queries Oracle, verifies the password and account role/status, and sets an HttpOnly session cookie. Slow login database work runs in a worker thread. `backend/auth/session.py` protects pages/APIs, checks request origins, and expires or invalidates sessions. Authenticated responses are not cached.

Run `node --test tests/login.test.cjs` for login JavaScript behavior tests. Python HTTP integration tests use isolated test accounts and do not modify Oracle records. Browser visual testing requires a connected browser.

## Member identifiers and audit history

New members must provide an ID/Roll number and Registration No. Each field is independently unique across members, including differences in letter case or surrounding whitespace. Leading zeros are preserved. Existing members retain their library IDs and show `Not assigned` for unknown academic identifiers; use **Members > Edit** to enter them or update name, department, phone, email and membership status. Both identifiers appear and can be searched in Membership and the issue-book member selector.

**Audit** is available to administrators. It records inserts, updates and deletes for members, books, authors, categories, loans, returns, fines, accounts and admin profiles. Each event includes the actor, time, record ID and before/after field values. API changes identify the signed-in user; direct database changes identify the Oracle user. Initial snapshots represent the state when tracking began, not earlier history. Passwords and hashes are excluded. Database triggers write audit events within the same transaction, so failed/rolled-back changes leave no history. Login/logout sessions are not database record changes and are not included.

`database/members_audit.sql` is included by the fresh setup before sample data is inserted. Academic identifiers and session are defined in `database/schema/members.sql`. Review history at `/audit`, filter by record type/action, search details and open **View details** to compare values. Dates display in Asia/Dhaka. Tests: `python -m unittest discover -s tests -v` and `node --test tests/login.test.cjs tests/members.test.cjs`.

## Connection recovery

Oracle XE can reject rapid parallel SQL*Plus connections with ORA-12520. Database commands now share a single process-wide slot with a brief handler-release delay. Transient connection errors retry up to twice; reads can also retry known disconnect errors. A connection-success marker prevents replaying writes after SQL has started. Mutation timeouts/disconnects are never automatically replayed.

Page data loads share one pending request batch, skip the redundant initial health query, retry temporary GET failures once and check recovery every five seconds. Browser online/visibility events also trigger recovery. Reads have a 60-second frontend timeout. Refresh failures cannot guarantee availability if Oracle/server is actually stopped; recovery resumes when the service is available.

Additional tests: `tests/test_connection_recovery.py` and `node --test tests/connection.test.cjs`.

## Overdue fines on the Fines page

The Fines page now includes active overdue loans, overdue days, today's estimated fine and a Return book action. Estimates use Oracle's calendar date and the same Tk 10/day rule as return_book_proc. Total outstanding combines overdue estimates with recorded unpaid fines, excludes paid fines, and avoids counting an issue twice. Returning a book records its final fine and moves it into return/payment history. An open fines page refreshes estimates every minute.

## Fast page data loading

Management pages use `/api/snapshot` to fetch books, members, loans, fines and metadata in one Oracle connection. Existing individual APIs remain available. Query definitions are reused through request-scoped collection; only read-only SELECT statements can be batched. Each output section is checked before decoding. No cached personal records are shown as fresh database data. Local measurement: six connections previously took about 1.40 seconds; one batched connection took about 0.24 seconds with identical results.

## Library notifications

Scheduled member reminders support a pre-due SMS/email and overdue email on days 1, 11, 21, …,
including current fine totals and the Tk 10/day rate. For a free email setup, use Gmail SMTP and
`DUE_REMINDER_CHANNEL=email`. Outbound delivery requires provider credentials and explicit
configuration; it is disabled by default. See [member reminder setup](docs/member-reminders.md).

The Fines page also shows total, today's and current month's collection. Total collection includes
legacy recorded paid balances. Day/month totals use dated payment receipts and Dhaka calendar
boundaries; legacy payments without dates cannot be assigned to a day or month.

Action lists prioritize overdue returns, unpaid fines, upcoming due dates and reservation pickups.
Active loans appear before returned history, with older due dates first. Fine records with an
outstanding balance appear before paid history, with larger balances first. Notifications follow
the same urgency order, even when a less urgent record is newer.

The header bell shows unread reservation pickups, return-date reminders, unpaid fine balances and current overdue fine
estimates. Admin and Librarian users see library-wide alerts; members see only their own alerts.
Select Reservations or Fines in the panel to filter alerts, then select an alert to open its page.
Mark all read changes the unread badge without resolving the loan, fine or reservation.
Return reminders begin three Dhaka calendar days before the due date and continue through the due
day. Each day has its own read state. Returned loans no longer produce reminders; overdue loans
show fine estimates instead. Members also see due/fine alerts directly on their dashboard.
The management overview includes detailed collection/member counts, upcoming return records and
member/book fine details, with recorded balances and overdue estimates shown separately.
Read identifiers are stored in this browser separately for each account; names and book details
are not stored. Paid fines and collected, cancelled or expired holds disappear on the next refresh.
Open staff pages refresh data about every 30 seconds; the member dashboard refreshes each minute.
New alerts show a toast after the initial load. Offline pages retain their last loaded alerts and
display a connection warning. These are in-app alerts while the page is open.

## Code organization

See [the module guide](docs/code-organization.md) for module responsibilities, request flows and formatting commands.
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code># PSTU Central Library</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>FastAPI and vanilla HTML/CSS/JavaScript library management application backed by Oracle XE 10g.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>## Run</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>Install Python dependencies with `python -m pip install -r backend/requirements.txt`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 8 | <code>Copy `.env.example` to `.env` and set your Oracle credentials. Environment variables override `.env`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 9 | <code>Oracle SQL*Plus defaults to `C:\oraclexe\app\oracle\product\10.2.0\server`; set `ORACLE_HOME` to override it.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 10 | <code>Run `powershell -ExecutionPolicy Bypass -File run.ps1`, then open http://localhost:8091.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 11 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 12 | <code>## Database</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>New loans are due **15 days after their issue date**, including reserved-copy pickups. Existing loans retain their recorded due dates.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>Circulation supports up to **3 active copies per member**, including multiple copies of one title. Select books and their physical copy numbers in the issue form; all selections are issued in one transaction. Return each loan separately. Existing stock receives copy numbers during migration; older returned loans display `Legacy copy` because their physical copy was never recorded. Attach the new numbers to the physical books to use them at the desk.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>The Fines page requires full payment of the outstanding balance, with an optional payment note. Custom amounts and partial payments are rejected. Existing partial payments and receipts are preserved; the next payment clears the entire remaining balance. Outstanding fines block new loans. Overdue fines remain Tk 10/day and are finalized when the copy is returned.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>For an existing installation, stop the app, run `python -m backend.upgrade_circulation`, and restart `run.ps1`. This upgrade preserves existing records and can be rerun; **do not run the reset/setup script to upgrade**. Fresh setup includes the same changes. Run rollback-only Oracle integration checks with `python -c &quot;from backend.database import ROOT,run_sql; print(run_sql(&#x27;SET SERVEROUTPUT ON\n@&#x27;+str(ROOT/&#x27;tests&#x27;/&#x27;circulation_oracle.sql&#x27;)))&quot;`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 21 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 22 | <code>Fresh setup uses `Setup-Database.bat` and requires typing `RESET`. It replaces project tables with the schema and sample data. Existing installations keep working until setup is explicitly run. Oracle DDL commits immediately.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>For a new demo installation, run `Setup-Database.bat`. It requires typing `RESET` because it drops existing library tables. Setup prompts for your administrator username and password; no shared login credentials are shipped. Configure the private Oracle credentials in .env before setup.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 25 | <code>Management passwords are salted PBKDF2 hashes. Existing plaintext management passwords are upgraded on successful login. Unused student/admin profile passwords in the original demo schema remain legacy fields.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 26 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 27 | <code>## Structure</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>- `backend/main.py`: application wiring and feature router registration.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 30 | <code>- `backend/routes/`: pages, catalogue, members, circulation, fines, audit and snapshot endpoints.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 31 | <code>- `backend/database.py`: configuration, SQL*Plus execution, Oracle errors and row decoding.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 32 | <code>- `backend/validation.py`: form and field validation.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 33 | <code>- `backend/auth/`: sessions, account routes and password hashing.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 34 | <code>- `database/setup.sql`: ordered fresh-install entry point; `database/schema/` holds the individual schema modules.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 35 | <code>- `database/members_audit.sql`: audit table, indexes, function and triggers, included before sample data.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 36 | <code>- `frontend/shared.js`: API client, live data, navigation and accessible dialogs.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 37 | <code>- `frontend/`: page-specific markup, styles and controllers.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 38 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 39 | <code>Database outages retain the last loaded records and block changes; reconnecting reloads live records. No demo changes are presented as persisted records.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 40 | <code>Sessions are in memory: run one server worker; restarting the server signs users out. Dates use Asia/Dhaka. SQL*Plus uses the installed database&#x27;s legacy character set; full Unicode support requires a compatible database/client configuration.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 41 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 42 | <code>## Student dashboard and reservations</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 43 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 44 | <code>Students sign in from the same login page and open `/student`. The member dashboard includes section navigation with a selected-section indicator, a welcome banner, summary cards, upcoming returns/pickups, filters for current/returned loans and available books, a searchable book-card catalogue and separate borrowing, reservation, fines and security sections. Generated library imagery is stored locally under `frontend/assets/member-*`; prompts are recorded in `frontend/assets/member-image-prompts.md`. They see the full searchable book catalogue, their own loans, due/return dates, fines and reservation history. Student sessions cannot access management APIs or other members&#x27; records.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 45 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 46 | <code>Students choose **Activate account** on the login page, enter their library Member ID (for example `PSTU-0001`) and registered 11-digit phone number, then set and confirm a password. Activation is one-time and requires an active membership. It creates a student account or activates an existing linked student account. It cannot reset an already activated account or re-enable a disabled account. After activation, sign in with Member ID and password; staff continue using their usernames. Students can change their password from their dashboard. **Forgot password** on the login page is available only to members: Member ID, ID/Roll, Registration No., registered phone and email must all match before a new password can be set. Recovery invalidates the member&#x27;s existing sessions and cannot change Admin/Librarian passwords. The library desk no longer creates student login credentials on the Reservations page.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 47 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 48 | <code>Admin and Librarian users have **Reservations** in the navigation and dashboard. The management overview organizes quick actions, six collection/circulation summary cards, desk priorities (overdue returns, reserved pickups and unpaid fines), recent circulation and inventory health. Shared management styling is in `frontend/polish.css`, with dashboard-specific styling in `frontend/admin.css`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 49 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 50 | <code>Reserving holds one available physical copy for exactly 72 hours. Other members cannot borrow that copy or remove it from stock. Available counts exclude active holds. The library desk uses **Issue reserved copy** when the member collects it; the hold becomes a normal 15-day loan. Students can cancel their own holds; staff can cancel any hold. A member may have up to three loans and active reservations together, with one active reservation per title. Disabled memberships and outstanding recorded fines block new reservations.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 51 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 52 | <code>Oracle runs an expiry job every minute, including while the web app is stopped. Queries and circulation guards release the hold at its exact deadline even between job runs. Open reservation pages refresh each minute. Reservation changes appear in Audit. Old fine receipts and existing library records are preserved.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 53 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 54 | <code>For an existing installation, stop the app and run `python -m backend.upgrade_circulation`, then restart it. Fresh setup includes reservations and linked demo student logins. Do not reset an existing database to upgrade. Rollback-only database tests are in `tests/recovery_oracle.sql`, `tests/activation_oracle.sql`, `tests/reservations_oracle.sql` and `tests/circulation_oracle.sql`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 55 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 56 | <code>## Verify</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 57 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 58 | <code>Run `python -m unittest discover -s tests -v` and `python -m compileall -q backend`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 59 | <code>Check JavaScript with `Get-ChildItem frontend -Filter *.js &#124; ForEach-Object { node --check $_.FullName }`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 60 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 61 | <code>## Login page flow</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 62 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 63 | <code>`frontend/login.html` defines the form and accessible controls. `frontend/login.css` provides the responsive glass card, autofill contrast, and background image. Save the campus photograph as `frontend/assets/pstu-library.jpg`; until that file exists, the existing library image is used.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>`frontend/login.js` sends one login request at a time, trims the username, handles timeouts and server errors, and redirects after a valid management-account response. `backend/validation.py` checks form size, encoding, duplicate fields, and required fields. `backend/auth/routes.py` queries Oracle, verifies the password and account role/status, and sets an HttpOnly session cookie. Slow login database work runs in a worker thread. `backend/auth/session.py` protects pages/APIs, checks request origins, and expires or invalidates sessions. Authenticated responses are not cached.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 66 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 67 | <code>Run `node --test tests/login.test.cjs` for login JavaScript behavior tests. Python HTTP integration tests use isolated test accounts and do not modify Oracle records. Browser visual testing requires a connected browser.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 68 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 69 | <code>## Member identifiers and audit history</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 70 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 71 | <code>New members must provide an ID/Roll number and Registration No. Each field is independently unique across members, including differences in letter case or surrounding whitespace. Leading zeros are preserved. Existing members retain their library IDs and show `Not assigned` for unknown academic identifiers; use **Members &gt; Edit** to enter them or update name, department, phone, email and membership status. Both identifiers appear and can be searched in Membership and the issue-book member selector.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 72 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 73 | <code>**Audit** is available to administrators. It records inserts, updates and deletes for members, books, authors, categories, loans, returns, fines, accounts and admin profiles. Each event includes the actor, time, record ID and before/after field values. API changes identify the signed-in user; direct database changes identify the Oracle user. Initial snapshots represent the state when tracking began, not earlier history. Passwords and hashes are excluded. Database triggers write audit events within the same transaction, so failed/rolled-back changes leave no history. Login/logout sessions are not database record changes and are not included.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 74 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 75 | <code>`database/members_audit.sql` is included by the fresh setup before sample data is inserted. Academic identifiers and session are defined in `database/schema/members.sql`. Review history at `/audit`, filter by record type/action, search details and open **View details** to compare values. Dates display in Asia/Dhaka. Tests: `python -m unittest discover -s tests -v` and `node --test tests/login.test.cjs tests/members.test.cjs`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 76 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 77 | <code>## Connection recovery</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 78 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 79 | <code>Oracle XE can reject rapid parallel SQL*Plus connections with ORA-12520. Database commands now share a single process-wide slot with a brief handler-release delay. Transient connection errors retry up to twice; reads can also retry known disconnect errors. A connection-success marker prevents replaying writes after SQL has started. Mutation timeouts/disconnects are never automatically replayed.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 80 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 81 | <code>Page data loads share one pending request batch, skip the redundant initial health query, retry temporary GET failures once and check recovery every five seconds. Browser online/visibility events also trigger recovery. Reads have a 60-second frontend timeout. Refresh failures cannot guarantee availability if Oracle/server is actually stopped; recovery resumes when the service is available.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 82 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 83 | <code>Additional tests: `tests/test_connection_recovery.py` and `node --test tests/connection.test.cjs`.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 84 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 85 | <code>## Overdue fines on the Fines page</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 86 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 87 | <code>The Fines page now includes active overdue loans, overdue days, today&#x27;s estimated fine and a Return book action. Estimates use Oracle&#x27;s calendar date and the same Tk 10/day rule as return_book_proc. Total outstanding combines overdue estimates with recorded unpaid fines, excludes paid fines, and avoids counting an issue twice. Returning a book records its final fine and moves it into return/payment history. An open fines page refreshes estimates every minute.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 88 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 89 | <code>## Fast page data loading</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 90 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 91 | <code>Management pages use `/api/snapshot` to fetch books, members, loans, fines and metadata in one Oracle connection. Existing individual APIs remain available. Query definitions are reused through request-scoped collection; only read-only SELECT statements can be batched. Each output section is checked before decoding. No cached personal records are shown as fresh database data. Local measurement: six connections previously took about 1.40 seconds; one batched connection took about 0.24 seconds with identical results.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 92 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 93 | <code>## Library notifications</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 94 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 95 | <code>Scheduled member reminders support a pre-due SMS/email and overdue email on days 1, 11, 21, …,</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 96 | <code>including current fine totals and the Tk 10/day rate. For a free email setup, use Gmail SMTP and</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 97 | <code>`DUE_REMINDER_CHANNEL=email`. Outbound delivery requires provider credentials and explicit</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 98 | <code>configuration; it is disabled by default. See [member reminder setup](docs/member-reminders.md).</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 99 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 100 | <code>The Fines page also shows total, today&#x27;s and current month&#x27;s collection. Total collection includes</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 101 | <code>legacy recorded paid balances. Day/month totals use dated payment receipts and Dhaka calendar</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 102 | <code>boundaries; legacy payments without dates cannot be assigned to a day or month.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 103 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 104 | <code>Action lists prioritize overdue returns, unpaid fines, upcoming due dates and reservation pickups.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 105 | <code>Active loans appear before returned history, with older due dates first. Fine records with an</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 106 | <code>outstanding balance appear before paid history, with larger balances first. Notifications follow</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 107 | <code>the same urgency order, even when a less urgent record is newer.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 108 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 109 | <code>The header bell shows unread reservation pickups, return-date reminders, unpaid fine balances and current overdue fine</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 110 | <code>estimates. Admin and Librarian users see library-wide alerts; members see only their own alerts.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 111 | <code>Select Reservations or Fines in the panel to filter alerts, then select an alert to open its page.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 112 | <code>Mark all read changes the unread badge without resolving the loan, fine or reservation.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 113 | <code>Return reminders begin three Dhaka calendar days before the due date and continue through the due</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 114 | <code>day. Each day has its own read state. Returned loans no longer produce reminders; overdue loans</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 115 | <code>show fine estimates instead. Members also see due/fine alerts directly on their dashboard.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 116 | <code>The management overview includes detailed collection/member counts, upcoming return records and</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 117 | <code>member/book fine details, with recorded balances and overdue estimates shown separately.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 118 | <code>Read identifiers are stored in this browser separately for each account; names and book details</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 119 | <code>are not stored. Paid fines and collected, cancelled or expired holds disappear on the next refresh.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 120 | <code>Open staff pages refresh data about every 30 seconds; the member dashboard refreshes each minute.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 121 | <code>New alerts show a toast after the initial load. Offline pages retain their last loaded alerts and</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 122 | <code>display a connection warning. These are in-app alerts while the page is open.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 123 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 124 | <code>## Code organization</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 125 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 126 | <code>See [the module guide](docs/code-organization.md) for module responsibilities, request flows and formatting commands.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
