$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
python -c "import fastapi, uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    python -m pip install -r backend\requirements.txt
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8091
