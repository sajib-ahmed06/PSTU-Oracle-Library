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
