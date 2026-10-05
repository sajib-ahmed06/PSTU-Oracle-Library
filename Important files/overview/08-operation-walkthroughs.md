# End-to-end operation walkthroughs

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
