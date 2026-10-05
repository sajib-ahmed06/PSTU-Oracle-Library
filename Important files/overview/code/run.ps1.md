# run.ps1

Project directory-তে গিয়ে dependencies import check/install করে localhost:8091-এ Uvicorn চালায়।

Source: [মূল file](../../run.ps1)। Snapshot 2026-10-04; 8 lines; SHA-256 `731d63a51e040db3986c9608b5e17df28169d74afd453e65b74ff5a37cb2f15a`।

## Function / object / element inventory

## সম্পূর্ণ original source

```powershell
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
python -c "import fastapi, uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    python -m pip install -r backend\requirements.txt
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8091
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>$ErrorActionPreference = &#x27;Stop&#x27;</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 2 | <code>Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 3 | <code>python -c &quot;import fastapi, uvicorn&quot; 2&gt;$null</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 4 | <code>if ($LASTEXITCODE -ne 0) {</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 5 | <code>    python -m pip install -r backend\requirements.txt</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 6 | <code>    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 7 | <code>}</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
| 8 | <code>python -m uvicorn backend.main:app --host 127.0.0.1 --port 8091</code> | Configuration, launcher instruction অথবা documentation text; এই file-এর দায়িত্ব অনুযায়ী ব্যবহার হয়। |
