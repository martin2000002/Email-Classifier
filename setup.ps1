# Root setup: create venv and install requirements
param(
    [string]$VenvPath = "venv",
    [string]$ReqPath = "requirements.txt"
)

$ErrorActionPreference = "Stop"

function Info($m){ Write-Host " -> $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host " [OK] $m" -ForegroundColor Green }
function Err($m){ Write-Host " [X] $m" -ForegroundColor Red }

Clear-Host
Write-Host "Unified Setup (root)" -ForegroundColor Magenta

try { $ver = python --version 2>&1; Info "Using $ver" } catch { Err "Python not found"; exit 1 }

if (-not (Test-Path $VenvPath)) {
  Info "Creating venv at '$VenvPath'"
  python -m venv $VenvPath
  Ok "venv created"
} else { Info "venv already exists at '$VenvPath'" }

if (-not (Test-Path $ReqPath)) { Err "requirements.txt not found at $ReqPath"; exit 1 }

Info "Upgrading pip"
& ".\$VenvPath\Scripts\python.exe" -m pip install --upgrade pip

Info "Installing requirements from $ReqPath"
& ".\$VenvPath\Scripts\python.exe" -m pip install -r $ReqPath
Ok "Dependencies installed"

Write-Host "Done. Activate with: .\\$VenvPath\\Scripts\\Activate.ps1" -ForegroundColor Yellow
