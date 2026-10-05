# Audit history ও transaction consistency

members_audit.sql audit_json_value function দিয়ে JSON string escaping করে: backslash, double quote ও control characters Unicode escapes। Null SQL value JSON null; numeric/date values snapshot-এ readable strings হতে পারে। before_data/after_data VARCHAR2(4000), dedicated JSON database datatype নয়।

নয়টি AFTER row triggers student/book/author/category/issue_book/return_book/fine/login_user/admin-এর INSERT/UPDATE/DELETE capture করে। One row change = one event; একটি issue operation inventory update এবং loan insert দুই বা বেশি event তৈরি করে। Audit writes autonomous transaction নয়: business rollback হলে events-ও rollback। Sequence values rollback হয় না।

Middleware session username ContextVar-এ বসায়; worker context propagation থাকে। run_sql DBMS_APPLICATION_INFO.SET_CLIENT_INFO দিয়ে actor Oracle session-এ পাঠায়। Trigger SYS_CONTEXT(USERENV,CLIENT_INFO) পড়ে, absent হলে Oracle USER। Legacy login password upgrade নিজের username actor set করে। Manual agent-request updates USER_REQUEST actor ব্যবহার করতে পারে; এটিকে actual admin username ধরে নেওয়া ঠিক নয়।

Initial records migration-এর সময় SNAPSHOT action-এ current values পায়। Existing event থাকলে সেই entity/record আর snapshot insert হয় না। এটি past edit history reconstruct করে না। Tracking শুরু হওয়ার আগের actions অজানা।

Admin /api/audit q/entity/action/page filters দেয়; query search literal INSTR, %/_ wildcard নয়। Page size 25; nested ROWNUM Oracle 10g pagination। actor ও JSON RAWTOHEX transport করে যাতে | অথবা newline field count না ভাঙে; Python cp1252 decode installed database charset ধরে। occurred_at UTC, frontend en-GB format+Asia/Dhaka display।

Audit detail modal keys union করে before/after পাশে দেখায়, differing fields highlight করে। Snapshots/insert-এর before এবং delete-এর after absent। Member name/contact/roll/reg, stock counts, loan dates/status, fine payments ও account role/status tracked। Password/hash fields বাদ। Password-only UPDATE event থাকতে পারে কিন্তু secret values comparison-এ আসবে না। Login/logout session events database record changes নয়, আলাদা events নেই। No export/retention policy/per-user timeline endpoint implemented।
