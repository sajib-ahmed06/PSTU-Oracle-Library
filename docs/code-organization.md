# Code organization

The application uses feature modules with explicit entry points. A page controller owns its UI;
its backend router validates the request and calls Oracle. Database routines enforce stock,
membership, reservation and payment rules within the transaction.

## Backend

| Module | Responsibility |
| --- | --- |
| `backend/main.py` | Create FastAPI, install authentication, register routers and serve static files. |
| `backend/routes/pages.py` | Management pages and database health. |
| `backend/routes/books.py` | Catalogue, physical copies and stock changes. |
| `backend/routes/members.py` | Member registration, profile edits and membership status. |
| `backend/routes/circulation.py` | Issue and return books. |
| `backend/routes/fines.py` | Outstanding fines, full payments and receipt history. |
| `backend/routes/snapshot.py` | Read the management dataset in one database connection. |
| `backend/routes/audit.py` | Administrator audit search and pagination. |
| `backend/auth/routes.py` | Login, logout, staff accounts and credential changes. |
| `backend/auth/member_access.py` | Public member activation and password recovery. |
| `backend/auth/validation.py` | Member identifiers and account credential validation. |
| `backend/auth/session.py` | Cookies, session lifetime, page/API access and origin checks. |
| `backend/auth/passwords.py` | Password hashing and verification. |
| `backend/reservations.py` | Student dashboard data, reserve/cancel/collect and student password changes. |
| `backend/database.py` | Oracle configuration, SQL*Plus execution, retries and result decoding. |
| `backend/validation.py` | Shared form decoding and field validation. |
| `backend/audit.py` | Actor attribution for database mutations. |
| `backend/reminders/` | Reminder eligibility/content, SMS/SMTP providers, scheduled checks and Oracle delivery claims. |

`main.py` keeps endpoint imports for callers that previously imported them there. New code should
import from the owning feature module. Tests patch database operations in that module.

## Frontend

Each management page has an HTML file and a controller with the same name. `index.html` uses
`dashboard.js`; `students.html` uses `students.js`.

| Module | Responsibility |
| --- | --- |
| `shared.js` | API requests, shared data, connection recovery, navigation and dialogs. |
| `notifications.js`, `notifications.css` | Role-scoped reservation/fine alerts, bell panel, unread identifiers and responsive styling. |
| `dashboard.js`, `admin.css` | Detailed collection and circulation metrics, upcoming returns and member fine records. |
| `member-dashboard.js` | Member overview, catalogue filters, borrowing, fines and password form. |
| `reservation-desk.js` | Staff reservation form and management view. |
| `reservations.js` | Select the page controller, refresh data and coordinate reservation actions. |
| `member-navigation.js` | Member section navigation and current-section indication. |
| `login.js`, `activate-account.js`, `forgot-password.js` | Public account form controllers. |
| `styles.css`, `polish.css` | Shared management layout and visual components. |
| `admin.css`, `student.css`, `login.css` | Dashboard and public account layouts. |
| `assets/` | Local images and recorded image-generation prompts. |

Protected pages load `notifications.js` before `shared.js`. The shared header owns the alert panel;
successful snapshots update its alerts, while outages retain the last loaded data. Staff snapshots
refresh roughly every 30 seconds while visible. The member controller supplies only its scoped
dashboard snapshot and refreshes each minute. Read identifiers are stored separately by account.
The notification module compares Dhaka calendar dates for the three-day return reminder window.
The member page renders the same due/fine items in a visible dashboard panel.

Student and reservation pages then load their page module and `reservations.js`.
The page module receives shared helpers through its context; the reservation coordinator owns
pending requests and action protection. API endpoints determine member identity from the session.

## Database

`database/setup.sql` includes these modules in order:

1. `schema/reset.sql` — clear the project schema for a confirmed fresh installation.
2. `schema/members.sql` — member tables, identifiers and membership routines.
3. `schema/catalogue.sql` — authors, categories, titles and catalogue indexes.
4. `schema/circulation.sql` — loans, returns and fines.
5. `schema/accounts.sql` — login accounts and supporting indexes.
6. `schema/routines.sql` — initial circulation triggers, routines and catalogue view.
7. Existing circulation, reservation, member-access and audit upgrade scripts.
8. `schema/sample_data.sql` — demo records.
9. `schema/verify.sql` — reject invalid database objects.

SQL*Plus `@@` resolves module paths relative to the including script. Run `Setup-Database.bat`
for a fresh installation; it requires `RESET`. For existing data, use
`python -m backend.upgrade_circulation`. Do not execute schema modules individually as migrations.

The schema split preserves the original SQL statement order. SQL*Plus commands, PL/SQL block
terminators and embedded SQL strings keep their original syntax.

## Development checks

Install application dependencies from `backend/requirements.txt`. Formatting tools are separate:

```powershell
python -m pip install -r requirements-dev.txt
npm install
python -m black backend tests "Important files/overview/tools"
npm run format
python -m black --check backend tests "Important files/overview/tools"
npm run format:check
python -m unittest discover -s tests
npm test
```

Black uses `pyproject.toml`; Prettier uses `.prettierrc.json`. Generated assets, private environment
configuration, scratch files and historical reference documents are excluded from web formatting.
Oracle rollback checks are listed in the root README.

Regenerate the project source references after module changes:

```powershell
python "Important files/overview/tools/generate_docs.py"
python "Important files/overview/tools/export_sql_reference.py"
```

When adding a feature, keep its request handlers in the relevant router, its page behavior in the
page controller, and its transactional rules in a named database upgrade script. Comments should
explain constraints, lock ordering or compatibility decisions that the code alone does not show.
