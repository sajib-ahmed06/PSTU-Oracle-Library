# database/setup.sql

Run fresh-install schema modules, upgrades, sample records and verification in dependency order.

Source: [মূল file](../../database/setup.sql)। Snapshot 2026-10-04; 19 lines; SHA-256 `4270b6666a4f38d02b5649942143935c22d499c78702fba336a55efee1e04e73`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
-- Fresh installation only: Setup-Database.bat requires RESET.
-- Run this entry point; schema modules depend on this order.

@@schema/reset.sql
@@schema/members.sql
@@schema/catalogue.sql
@@schema/circulation.sql
@@schema/accounts.sql
@@schema/routines.sql
-- Audit tables and triggers must exist before loading sample records.
@@circulation_upgrade.sql
@@reservations_upgrade.sql
@@student_activation_upgrade.sql
@@members_audit.sql
@@reservations_audit_upgrade.sql
@@reminders_upgrade.sql

@@schema/sample_data.sql
@@schema/verify.sql
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Fresh installation only: Setup-Database.bat requires RESET.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>-- Run this entry point; schema modules depend on this order.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 3 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 4 | <code>@@schema/reset.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 5 | <code>@@schema/members.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 6 | <code>@@schema/catalogue.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 7 | <code>@@schema/circulation.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 8 | <code>@@schema/accounts.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 9 | <code>@@schema/routines.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 10 | <code>-- Audit tables and triggers must exist before loading sample records.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 11 | <code>@@circulation_upgrade.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 12 | <code>@@reservations_upgrade.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 13 | <code>@@student_activation_upgrade.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 14 | <code>@@members_audit.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 15 | <code>@@reservations_audit_upgrade.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 16 | <code>@@reminders_upgrade.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>@@schema/sample_data.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 19 | <code>@@schema/verify.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
