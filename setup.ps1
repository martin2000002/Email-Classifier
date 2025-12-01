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
Write-Host "SETUP" -ForegroundColor Magenta

try { $ver = python --version 2>&1; Info "Using $ver" } catch { Err "Python not found"; exit 1 }

if (-not (Test-Path $VenvPath)) {
  Info "Creating venv at '$VenvPath'"
  python -m venv $VenvPath
  Ok "venv created"

  if (-not (Test-Path $ReqPath)) { Err "requirements.txt not found at $ReqPath"; exit 1 }

  Info "Upgrading pip"
  & ".\$VenvPath\Scripts\python.exe" -m pip install --upgrade pip

  Info "Installing requirements from $ReqPath"
  & ".\$VenvPath\Scripts\python.exe" -m pip install -r $ReqPath
  Ok "Dependencies installed"
} else { 
  Info "venv already exists at '$VenvPath'. Skipping setup steps..." 
}

Write-Host "Done. Activate with: .\\$VenvPath\\Scripts\\Activate.ps1" -ForegroundColor Yellow

# --- Interactive Menu ---
while ($true) {
    Write-Host "`n"
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "       EMAIL CLASSIFIER - CONTROL PANEL       " -ForegroundColor White -BackgroundColor DarkBlue
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host " [1] Start Backend API (New Terminal)" -ForegroundColor Green
    Write-Host " [2] Open Frontend (Default Browser)" -ForegroundColor Green
    Write-Host " [3] Retrain Model (Current Window)" -ForegroundColor Green
    Write-Host " [4] Run Tests (pytest -q)" -ForegroundColor Green
    Write-Host " [5] Exit" -ForegroundColor Red
    Write-Host "==============================================" -ForegroundColor Cyan
    
    $choice = Read-Host " Select an option"
    
    switch ($choice) {
        "1" {
            Write-Host " >> Launching Backend API..." -ForegroundColor Yellow
            # Launch new PowerShell, activate venv, cd to backend, and run uvicorn
            $activate = "$PSScriptRoot\$VenvPath\Scripts\Activate.ps1"
            $backendDir = "$PSScriptRoot\code\backend"
            $cmd = "& '$activate'; Set-Location '$backendDir'; python -m uvicorn main:app --reload"
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "$cmd"
        }
        "2" {
            Write-Host " >> Opening Frontend..." -ForegroundColor Yellow
            $html = "$PSScriptRoot\code\frontend\index.html"
            Start-Process $html
        }
        "3" {
            Write-Host " >> Retraining Model..." -ForegroundColor Yellow
            $py = "$PSScriptRoot\$VenvPath\Scripts\python.exe"
            $backendDir = "$PSScriptRoot\code\backend"
            Push-Location $backendDir
            try {
                & $py "train.py"
            } finally {
                Pop-Location
            }
        }
        "4" {
            Write-Host " >> Running Tests..." -ForegroundColor Yellow
            $pytest = "$PSScriptRoot\$VenvPath\Scripts\pytest.exe"
            & $pytest -q
        }
        "5" {
            Write-Host "Bye!" -ForegroundColor Cyan
            exit 0
        }
        default {
            Write-Host "Invalid option." -ForegroundColor Red
        }
    }
}
