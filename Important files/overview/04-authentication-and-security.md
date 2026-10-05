# Authentication, roles ও sessions

Login flow: username/password form → body validation → username search → password verification → management role ADMIN/LIBRARIAN check → ACTIVE account check → legacy password hash upgrade প্রয়োজনে → session token creation → cookie response → frontend valid username/role response যাচাই করে dashboard redirect। STUDENT account management dashboard access পায় না; student self-service portal নেই।

PBKDF2-HMAC-SHA256: salt = 16 random bytes, iterations = 260000, digest Base64; format `pbkdf2$rounds$salt$digest`। Verification stored rounds 100000–1000000 range check করে। hmac.compare_digest ব্যবহার হয়। Legacy plaintext stored password login-এ verify হওয়ার পরে hash-এ বদলানো হয়। admin/student profile tables-এর unused legacy password fields current authentication source নয়; login_user password authoritative।

Session dictionary process memory-তে: user_id, username, user_type, expires। Cookie library_session; lifetime আট ঘণ্টা; HttpOnly, SameSite=strict; HTTPS request হলে Secure। Restart হলে sessions হারায়। Shared session backend নেই বলে multiple workers ব্যবহার করলে session lookup mismatch হতে পারে। Expired session access অথবা new session creation-এ cleanup হয়। Logout token ও cookie delete করে। Disabled/deleted librarian-এর sessions invalidated। Admin credential update অন্য sessions invalidates করে বর্তমান token পুনরায় stores। Session expiry sliding refresh নয়।

Middleware permits login, member activation, member password recovery, health and static assets without an authenticated session. Protected APIs return 401 without a session; protected pages redirect to login. STUDENT sessions can access their own dashboard and reservation operations, while management pages require staff access. Write requests with an Origin header must match the current origin. Authenticated responses use Cache-Control: no-store.

Roles: ADMIN সব management, account controls ও audit; LIBRARIAN library operations, account/audit access নেই; STUDENT management login reject। Frontend hidden link permission enforcement নয়; backend require_admin authoritative। HTML escaping data-as-HTML risk কমায়; audit details passwords/hashes বাদ দেয়।

বর্তমান সীমা: rate limiting/account lockout নেই; password minimum মাত্র চার characters; permission/auth state live database-এ প্রতি request revalidate নয়; direct SQL account disable/delete করলে in-memory sessions immediate invalidated হয় না। TLS deployment/session persistence/production secret provisioning এখানে implemented নয়। Audit schema owner records edit/drop করতে পারে; tamper-proof audit service নয়।
