# Backend ও input validation

main.py creates FastAPI, installs authentication, registers feature routers and mounts frontend assets. backend/routes separates pages, books, members, circulation, fines, snapshot and audit. Authentication routes live under backend/auth; reservations.py provides member-scoped dashboard data and reservation operations. Staff account management and audit require ADMIN access.

Form content frontend থেকে URLSearchParams(new FormData(form)) হয়। form_data request.body সম্পূর্ণ পড়ে, তারপর 16384-byte limit checks; এটি streaming upload size enforcement নয়। সর্বোচ্চ 30 fields; invalid raw/percent-encoded UTF-8, malformed % escapes ও duplicate keys reject। JSON/multipart parsing helper নয়। required() None/blank/whitespace reject করে। positive_number integer ও >0 চায়। text_field সর্বোচ্চ UTF-8 byte length checks; এটি Oracle character-set bytes-এর সরাসরি measurement নয়।

member_details name/department/email সর্বোচ্চ 100 bytes; email lowercase + simple structural regex; phone ঠিক 11 ASCII digits; roll ও registration uppercase, সর্বোচ্চ 40 bytes, allowed ASCII letters/digits/dot/slash/underscore/hyphen। Domain deliverability, country-specific email policy বা unique name requirement নেই।

Add member-এ phone precheck থাকে, তবে race-safe uniqueness Oracle indexes/constraints enforce করে। Full edit-এ name, department, phone, email, roll/reg, membership_status mandatory। Student row SELECT FOR UPDATE lock হয়; ACTIVE→DISABLED-এর আগে issued books ও unpaid fines checks। Internal student_id edit হয় না। Identity-only endpoint compatibility হিসেবে আছে; UI এখন full /edit call করে।

database.py SQL*Plus stdin-এ CONNECT ও script পাঠায়; password subprocess argv-তে দেয় না। SET DEFINE OFF ampersand substitution বন্ধ করে; SQLBLANKLINES ON blank SQL lines নেয়। WHENEVER SQLERROR ... ROLLBACK ও OSERROR handling থাকে। quote() apostrophe escape/control-character reject করে; bind variables নেই। SELECT output fields | delimiter, ~ null marker; কিছু values REPLACE দিয়ে | সরায়, audit RAWTOHEX দিয়ে delimiter/newlines এড়ায়।

HTTP errors: input 400, unauthenticated API 401, forbidden admin/role/origin 403, missing database record 404, conflicts/domain rule 409, too-large form 413, malformed row format 502, database failure 503, timeout 504। Missing SQLPlus path বর্তমানে 500। Generic Oracle failures server log-এ যায়; user-কে internal error detail সাধারণত দেওয়া হয় না।

Login and async library mutation SQL work now runs in run_in_threadpool. Some account create/change operations still contain synchronous database work. SQLPlus commands share one slot to avoid XE listener overload.
