# ═══════════════════════════════════════════════════════════════════════════
# AgriSenseGuardian Uses NASA POWER By Default - This Is Only For Advanced Users
# ═══════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Copernicus CDS API Configuration Helper (OPTIONAL)       ║" -ForegroundColor Cyan
Write-Host "║     AgriSenseGuardian - Advanced Satellite Data Setup        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANT: This Setup Is OPTIONAL!" -ForegroundColor Yellow
Write-Host ""
Write-Host "AgriSenseGuardian Already Uses NASA POWER For Satellite Data." -ForegroundColor White
Write-Host "NASA POWER Provides Excellent Agricultural Data With Zero Setup." -ForegroundColor White
Write-Host ""
Write-Host "Only Continue If You Need Advanced Features Like:" -ForegroundColor Gray
Write-Host "  • Soil Moisture Analysis" -ForegroundColor Gray
Write-Host "  • NDVI Vegetation Indices" -ForegroundColor Gray
Write-Host "  • Evapotranspiration Rates" -ForegroundColor Gray
Write-Host ""

$Continue = Read-Host "Do You Want To Continue With Copernicus Setup? (y/N)"
if ($Continue -notmatch '^[Yy]') {
    Write-Host ""
    Write-Host "✅ No Problem! AgriSenseGuardian Will Use NASA POWER (Recommended)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press Any Key To Exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Check If CDS API Is Installed
Write-Host "Checking CDS API Installation..." -ForegroundColor Yellow
try {
    python -c "import cdsapi" 2>$null
    Write-Host "✅ CDS API Package Found" -ForegroundColor Green
} catch {
    Write-Host "❌ CDS API Not Installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing CDS API..." -ForegroundColor Yellow
    pip install cdsapi
    Write-Host "✅ CDS API Installed Successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Get API Credentials From User
Write-Host "📋 You Need Your CDS API Credentials" -ForegroundColor Cyan
Write-Host ""
Write-Host "To Get Your Credentials:" -ForegroundColor White
Write-Host "  1. Visit: https://cds.climate.copernicus.eu/" -ForegroundColor Gray
Write-Host "  2. Login (Or Register If New User)" -ForegroundColor Gray
Write-Host "  3. Click Your Username → 'Your Profile'" -ForegroundColor Gray
Write-Host "  4. Scroll To 'Personal Access Token' Section" -ForegroundColor Gray
Write-Host "  5. Copy The API Key (UUID Format)" -ForegroundColor Gray
Write-Host ""

# Prompt For API Key
$APIKey = Read-Host "Enter Your CDS API Key (Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"
if ([string]::IsNullOrWhiteSpace($APIKey)) {
    Write-Host "❌ API Key Cannot Be Empty. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Define .cdsapirc File Path
$ConfigPath = Join-Path $env:USERPROFILE ".cdsapirc"

# Create .cdsapirc File Content
$ConfigContent = @"
url: https://cds.climate.copernicus.eu/api
key: ${APIKey}
"@

# Write Configuration File
Write-Host "Creating Configuration File..." -ForegroundColor Yellow
try {
    $ConfigContent | Out-File -FilePath $ConfigPath -Encoding ASCII -Force
    Write-Host "✅ Configuration File Created: $ConfigPath" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed To Create Configuration File: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Verify File Creation
Write-Host "Verifying Configuration..." -ForegroundColor Yellow
if (Test-Path $ConfigPath) {
    Write-Host "✅ File Exists At: $ConfigPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "File Contents:" -ForegroundColor Cyan
    Get-Content $ConfigPath | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
} else {
    Write-Host "❌ File Not Found. Something Went Wrong." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Test CDS API Connection
Write-Host "Testing CDS API Connection..." -ForegroundColor Yellow
$TestScript = @"
import cdsapi
try:
    client = cdsapi.Client()
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
"@

$TestResult = python -c $TestScript 2>&1
if ($TestResult -like "*SUCCESS*") {
    Write-Host "✅ CDS API Connection Successful!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Connection Test Results:" -ForegroundColor Yellow
    Write-Host "   $TestResult" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Note: You May Need To Accept Dataset Terms At:" -ForegroundColor Cyan
    Write-Host "      https://cds.climate.copernicus.eu/datasets" -ForegroundColor Gray
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Next Steps
Write-Host "📝 NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Accept Dataset Terms (REQUIRED Before Data Download):" -ForegroundColor White
Write-Host "   • Visit: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land" -ForegroundColor Gray
Write-Host "   • Click 'Download Data' Tab" -ForegroundColor Gray
Write-Host "   • Accept The Licence Agreement" -ForegroundColor Gray
Write-Host ""
Write-Host "2. (Optional) Update AgriSenseGuardian .env File:" -ForegroundColor White
Write-Host "   COPERNICUS_API_KEY=${APIKey}" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run AgriSenseGuardian:" -ForegroundColor White
Write-Host "   python Main.py" -ForegroundColor Gray
Write-Host ""

Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║           ✅ Setup Complete! Ready For Satellite Data!        ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Pause To Let User Read
Write-Host "Press Any Key To Exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")