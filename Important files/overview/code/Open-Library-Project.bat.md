# Open-Library-Project.bat

Minimized PowerShell server launcher শুরু করে আট সেকেন্ড পরে browser-এ localhost:8091 খোলে।

Source: [মূল file](../../Open-Library-Project.bat)। Snapshot 2026-10-04; 14 lines; SHA-256 `3dbdf5850c68c577787db56db57b02a7bd7480d0066ee606fb5589a08d9dee03`।

## Function / object / element inventory

## সম্পূর্ণ original source

```bat
@echo off
setlocal
cd /d "%~dp0"

if not exist "frontend\index.html" (
    echo Error: frontend\index.html was not found.
    pause
    exit /b 1
)

start "PSTU Library Server" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1"
timeout /t 8 /nobreak >nul
start "" "http://localhost:8091"
exit /b 0
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>@echo off</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 2 | <code>setlocal</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 3 | <code>cd /d &quot;%~dp0&quot;</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>if not exist &quot;frontend\index.html&quot; (</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 6 | <code>    echo Error: frontend\index.html was not found.</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 7 | <code>    pause</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 8 | <code>    exit /b 1</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 9 | <code>)</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>start &quot;PSTU Library Server&quot; /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File &quot;%~dp0run.ps1&quot;</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 12 | <code>timeout /t 8 /nobreak &gt;nul</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 13 | <code>start &quot;&quot; &quot;http://localhost:8091&quot;</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 14 | <code>exit /b 0</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
