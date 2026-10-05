# Setup, configuration ও launcher

1. Oracle XE service/listener ও SQL*Plus install থাকতে হবে। Default home `C:\oraclexe\app\oracle\product\10.2.0\server`। `ORACLE_HOME` environment variable দিয়ে override হয়।
2. `python -m pip install -r backend/requirements.txt` চালাও। Python environment-এ FastAPI/Uvicorn থাকতে হবে; tests অতিরিক্ত httpx লাগে না।
3. `.env.example` থেকে `.env` তৈরি করো। DB_USER, DB_PASSWORD, DB_DSN database.py পড়ে। Process environment file values-এর ওপর priority পায়। Current parser পুরো dotenv specification নয়; quotes/export/multiline syntax বিশেষভাবে support করে না। ORACLE_HOME process environment থেকে path তৈরি হওয়ার সময় পড়া হয়, .env-এর ORACLE_HOME দিয়ে path override হয় না।
4. Existing database হলে `python backend/setup_database.py --migrate`। Upgrade sequence advance ও indexes/features যোগ করে; existing library records delete করে না। Oracle DDL implicit commit হয়; failure-এ earlier DDL rollback হয় না। Script idempotent column/index checks রাখে, কিন্তু backup ছাড়া migration undo সুবিধা নেই।
5. Demo reset হলে `Setup-Database.bat`; RESET type করা আবশ্যক। Existing library tables/audit history মুছে sample records ফেরত আসে। Bootstrap existing CONFIGURED_SCHEMA password-ও public demo default-এ reset/unlock করে। Custom schema credentials নিয়ে demo setup স্বয়ংক্রিয় parameterized নয়।
6. `powershell -ExecutionPolicy Bypass -File run.ps1` অথবা launcher batch। Server `127.0.0.1:8091`-এ single worker। Browser URL `http://localhost:8091`। Batch আট সেকেন্ড wait করে; server readiness polling নয়।

tnsnames.ora-তে XE = TCP 127.0.0.1:1521 / service XE / dedicated server। sqlnet.ora application connections-এ OS authentication NONE; setup local SYSDBA attempt TNS_ADMIN বাদ দেয়। NLS_LANG WE8MSWIN1252; Bengali/Unicode data preservation নিশ্চিত করা হয়নি।

Login demo seed <private-administrator-login>; সেটি current account password-এর নিশ্চয়তা নয়, কারণ Accounts page দিয়ে password বদলানো যায়। এই public seed value source-এ আছে; real private .env এই documents-এ নেই।

`.vscode/settings.json` installed interpreter এবং site-packages path ধরে Pylance resolve করে। অন্য PC-তে paths বদলাতে হবে। Browser এক origin-এ রাখো: localhost ও 127.0.0.1 আলাদা cookie hosts।
