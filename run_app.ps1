# Run the FastAPI app using the venv in AppData (avoids OneDrive .venv issues)
$ErrorActionPreference = "Stop"
$venvPython = "$env:LOCALAPPDATA\GenAI-venv\Scripts\python.exe"
$projectRoot = $PSScriptRoot

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating venv at $env:LOCALAPPDATA\GenAI-venv ..."
    python -m venv "$env:LOCALAPPDATA\GenAI-venv"
    & "$venvPython" -m pip install -r "$projectRoot\requirements.txt" -q
}
Set-Location $projectRoot
& $venvPython run.py
