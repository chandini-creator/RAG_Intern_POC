# Activate the GenAI venv (lives in AppData to avoid OneDrive .venv errors)
$activate = "$env:LOCALAPPDATA\GenAI-venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    . $activate
    Write-Host "Activated GenAI-venv. Run: python run.py"
} else {
    Write-Host "Venv not found. Run: .\run_app.ps1 (it will create the venv)"
}
