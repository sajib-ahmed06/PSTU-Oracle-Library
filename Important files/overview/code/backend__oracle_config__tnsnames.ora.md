# backend/oracle_config/tnsnames.ora

XE alias-কে localhost TCP port 1521 এবং XE service-এর সঙ্গে যুক্ত করে।

Source: [মূল file](../../backend/oracle_config/tnsnames.ora)। Snapshot 2026-10-04; 9 lines; SHA-256 `3b3af93f12d5024b2566ecc241c5e36e3ffbd5863921e426d7f18468603e751d`।

## Function / object / element inventory

## সম্পূর্ণ original source

```text
XE =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = XE)
    )
  )
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>XE =</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 2 | <code>  (DESCRIPTION =</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 3 | <code>    (ADDRESS = (PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 4 | <code>    (CONNECT_DATA =</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 5 | <code>      (SERVER = DEDICATED)</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 6 | <code>      (SERVICE_NAME = XE)</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 7 | <code>    )</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 8 | <code>  )</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
