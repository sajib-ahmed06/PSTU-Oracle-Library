# Tests, verification ও maintenance

Python: `python -m unittest discover -s tests -v`। JavaScript: `node --test tests/login.test.cjs tests/members.test.cjs`। Python syntax: `python -m compileall -q backend`। PowerShell JavaScript syntax: `Get-ChildItem frontend -Filter *.js | ForEach-Object { node --check $_.FullName }`।

test_regressions.py password hash/legacy, quoting/control input, forms, session invalidation, row decoding, missing fines ও Oracle error/rollback configuration checks করে। test_login_api.py isolated FastAPI/Uvicorn server + stdlib HTTP cookie client দিয়ে real HTTP workflow checks করে; fake account rows ব্যবহার করে, real Oracle records বদলায় না। Slow login query চলার সময় health response test threadpool behavior checks।

test_members_audit.py member normalization/required IDs/full edit validation, generated SQL/locks/disabling protections, duplicate error messages, admin-only audit, hex/JSON pagination ও actor propagation পরীক্ষা করে। login.test.cjs Node vm-এ DOM/fetch stubs দিয়ে visibility/success/error/repeated submission checks। members.test.cjs directory fields/search checks; browser layout validation নয়।

Source tests-এর কিছু SQL assertions implementation details check করে; এর পাশাপাশি session/API/encoding behavior tests আছে। Live Oracle transactional verification আগের কাজের সময় করা হয়েছে; ordinary test suite সব schema/trigger paths live Oracle-এ স্বয়ংক্রিয় চালায় না। Browser screenshot/visual QA-এর callable browser connection পাওয়া যায়নি। Passing tests সব future bugs নেই এমন guarantee নয়।

Maintenance: new member field হলে validation, form, prefill, API list/create/edit, schema migration ও audit student snapshot বদলাতে হবে। নতুন table audit করতে হলে trigger/snapshot/entity whitelist/frontend labels add করতে হবে। New endpoint permission middleware/require_admin ও frontend navigation দুইটাই review করো। Business rules frontend-only নয়, backend/database-এ রাখো।

Docs refresh: `python 'Important files/overview/tools/generate_docs.py'`। Generator app import/SQL execute করে না; source files read করে overview markdown/index/manifest overwrite করে। Schema/API changes-এর পরে curated chapters manually review করো; generated line/function inventories নতুন source তুলে নেয়, কিন্তু narrative business explanation স্বয়ংক্রিয় semantic proof নয়।
