# backend/oracle_config/sqlnet.ora

Application connection-এর Windows OS authentication বন্ধ রাখে। Setup-এর স্থানীয় SYSDBA path এই TNS configuration বাদ দেয়।

Source: [মূল file](../../backend/oracle_config/sqlnet.ora)। Snapshot 2026-10-04; 2 lines; SHA-256 `df6d2c8243cd890874b46e55422d9ffa8cb0999a9f5597e08825a09529fbad23`।

## Function / object / element inventory

## সম্পূর্ণ original source

```text
SQLNET.AUTHENTICATION_SERVICES = (NONE)
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>SQLNET.AUTHENTICATION_SERVICES = (NONE)</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
