# PSTU Library — A to Z Project Overview

Documentation snapshot: **2026-10-04 (Asia/Dhaka)**। বাংলায় project explanation, পূর্ণ source, function inventory, line references এবং operational guide।

## পড়ার ক্রম

1. [Project ও architecture](01-project-and-architecture.md)
2. [Setup ও configuration](02-setup-and-configuration.md)
3. [Backend ও validation](03-backend-and-validation.md)
4. [Authentication ও security](04-authentication-and-security.md)
5. [Database ও business rules](05-database-and-business-rules.md)
6. [Frontend ও design](06-frontend-and-design.md)
7. [Audit ও transactions](07-audit-and-transactions.md)
8. [End-to-end workflows](08-operation-walkthroughs.md)
9. [Tests ও maintenance](09-testing-and-maintenance.md)
10. [Troubleshooting ও limitations](10-troubleshooting-and-limitations.md)
11. [প্রতিটি file-এর পূর্ণ code ও line-by-line guide](11-file-code-index.md)
12. [সব endpoints-এর reference](12-api-reference.md)
13. [Images, runtime files ও exclusions](13-assets-and-runtime-files.md)
14. [প্রতিটি database field ও response schema](14-data-dictionary-and-responses.md)
15. [Code concepts ও dependencies glossary](15-code-concepts-and-dependencies.md)

## Coverage ও refresh

112টি text/source/configuration file-এর পূর্ণ code ও প্রতিটি line-এর reading notes; 7টি image asset-এর inventory। API documentation source decorators থেকে তৈরি। manifest.json-এ paths/line counts/SHA-256 আছে।

Private .env credentials, generated caches/logs ও historical local backups-এর full contents included নয়; তাদের ভূমিকা document করা হয়েছে। কোনো live personal data dump নেই। Public sample SQL অপরিবর্তিতভাবে code guide-এ আছে।

Refresh: `python 'Important files/overview/tools/generate_docs.py'`। Current source snapshot বদলালে docs regenerate করো এবং curated narrative review করো। [Generator পূর্ণ code](code/overview__tools__generate_docs.py.md)।

Application behavior অথবা database records এই documentation task-এ পরিবর্তন করা হয়নি। Source guide-এর syntax notes ও curated business explanation একসঙ্গে পড়লে code বুঝতে সুবিধা হবে।

## SQL references

- [Output দেখার queries ও backend SQL templates](queries.md)
- [Database-এর সম্পূর্ণ SQL code](database-full-code.md)

এই দুই reference update করতে `python 'Important files/overview/tools/export_sql_reference.py'` চালান।
