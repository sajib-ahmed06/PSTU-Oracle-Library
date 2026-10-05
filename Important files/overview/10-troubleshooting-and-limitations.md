# Troubleshooting ও বর্তমান limitations

| Symptom | কারণ/সমাধান |
| --- | --- |
| Pylance FastAPI missing import | VS Code interpreter installed FastAPI environment-এর সঙ্গে মেলাও; .vscode absolute paths local PC-এর; reload language server/window |
| SQLPlus not found | ORACLE_HOME path ও bin/sqlplus.exe check; setup এবং runtime path environment-driven |
| Oracle unavailable | XE service/listener, port 1521, TNS alias এবং DB credentials check; health endpoint actual SELECT চালায় |
| Invalid objects after migration | USER_ERRORS ও USER_OBJECTS inspect; migration recompiles dependent student trigger/issue/return procedures |
| Unique identifier error | অন্য member একই normalized roll/reg ব্যবহার করছে; case বা whitespace বদলিয়ে bypass হয় না |
| Cannot disable membership | Active loan return এবং unpaid fines pay করতে হবে; Edit status ও quick toggle একই rules রাখে |
| Cannot issue another book | Existing loan/unpaid fines/disabled membership/zero stock checks |
| Login loops after restart | Sessions in memory; login আবার করতে হবে; multiworker/shared sessions নেই |
| Background পুরোনো | pstu-library.jpg asset আছে কি না এবং Ctrl+F5; CSS fallback পুরোনো library image |
| UI old Edit IDs | Server restart এবং cache-versioned students.js reload; button current source Edit |
| Audit empty/forbidden | Admin login চাই; filters clear করো; feature migration/app restart check |

সীমাবদ্ধতা source অনুযায়ী: SQLPlus per request subprocess overhead; bind variables/connection pool নেই; dependencies unpinned; in-memory sessions; weak minimum password policy; no rate limiting; legacy unused plaintext fields; Windows/Oracle10g assumptions; Unicode transport legacy charset; no delete-member workflow; no automatic academic-ID sequence assignment for newly added members; no backup scheduler/export/retention; audit schema owner tampering prevention নেই।

Setup reset-এর sample members আর live sequence-assigned roll/reg আলাদা। Roll/reg uniqueness independent: একটি member-এর roll অন্য member-এর registration string-এর সমান হওয়া দুই-column cross-uniqueness দিয়ে আটকানো হয়নি। দুই roll কখনো এক নয় এবং দুই registration কখনো এক নয়।

Security error parsing output-এর মধ্যে ORA-/SP2- substring খোঁজে; user text-এ error-looking substring থাকলে false error classification সম্ভব। Delimiter/null-marker transport application convention; generic full-Unicode JSON database driver নয়। Main long SQL strings, repeated membership rules এবং identity-only compatibility endpoint future refactor candidates। Documentation এগুলো implementation facts হিসেবে বলে; এই task-এ application behavior বদলানো হয়নি।
