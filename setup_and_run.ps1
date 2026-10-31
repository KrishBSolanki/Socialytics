# setup_and_run.ps1
# =======================================================
# One-click: Install all dependencies → Train model → Launch app
# Run from project root:  .\setup_and_run.ps1
# =======================================================

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "  Social Media Sentiment Analysis Setup" -ForegroundColor Cyan
Write-Host "==========================================`n" -ForegroundColor Cyan

$python = "python"
# Check if python command works; if not, check common paths or py launcher
try {
    $test = & $python --version 2>&1
    if ($LASTEXITCODE -ne 0 -or $test -match "error|cannot be accessed") {
        throw "python alias failed"
    }
} catch {
    if (Test-Path "$env:LOCALAPPDATA\Python\bin\python.exe") {
        $python = "$env:LOCALAPPDATA\Python\bin\python.exe"
    } elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
        $python = "py"
    }
}

# ── Verify Python ─────────────────────────────────────────
Write-Host "[1/3] Checking Python..." -ForegroundColor Yellow
$pyVer = & $python --version 2>&1
Write-Host "      $pyVer" -ForegroundColor Green

# ── Install packages one by one ───────────────────────────
Write-Host "`n[2/3] Installing packages (this may take several minutes)..." -ForegroundColor Yellow

$packages = @(
    "pandas",
    "numpy",
    "scipy",
    "scikit-learn",
    "joblib",
    "nltk",
    "matplotlib",
    "seaborn",
    "plotly",
    "wordcloud",
    "streamlit",
    "requests",
    "tqdm"
)

foreach ($pkg in $packages) {
    Write-Host "      Installing $pkg..." -NoNewline
    $result = & $python -m pip install $pkg --timeout 120 --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " WARN (may already be installed)" -ForegroundColor Yellow
        Write-Host "      $result" -ForegroundColor DarkGray
    }
}

# ── Download NLTK data ────────────────────────────────────
Write-Host "`n      Downloading NLTK data..." -NoNewline
& $python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('stopwords', quiet=True); print('OK')"

# ── Train Model ───────────────────────────────────────────
Write-Host "`n[3/3] Training the sentiment model..." -ForegroundColor Yellow
& $python train_model.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Training failed. Check error messages above." -ForegroundColor Red
    exit 1
}

# ── Launch App ────────────────────────────────────────────
Write-Host "`n===========================================" -ForegroundColor Cyan
Write-Host "  Launching Streamlit App..." -ForegroundColor Cyan
Write-Host "  Open: http://localhost:8501" -ForegroundColor Green
Write-Host "===========================================`n" -ForegroundColor Cyan

& $python -m streamlit run app.py
