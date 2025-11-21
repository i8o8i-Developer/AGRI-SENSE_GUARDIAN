# 🚀 AgriSenseGuardian — Complete Setup Guide

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    COMPREHENSIVE INSTALLATION GUIDE                       ║
║              From Zero To Running In 15 Minutes                           ║
║                  For Windows, Linux, And macOS                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## Prerequisites

### **System Requirements**

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Operating System** | Windows 10, Ubuntu 20.04, macOS 11 | Windows 11, Ubuntu 22.04, macOS 13+ |
| **Python Version** | 3.11.0 | 3.11.5+ Or 3.12+ |
| **RAM** | 2 GB | 4 GB+ |
| **Disk Space** | 500 MB | 1 GB+ |
| **Internet Connection** | Required For API Calls | High-Speed Recommended |

### **Required Software**

#### **1. Python 3.11+**

**Check If Already Installed:**

```powershell
# Windows PowerShell
python --version

# Linux/macOS
python3 --version
```

**If Not Installed:**

- **Windows:** Download From [python.org](https://www.python.org/downloads/) (Check "Add Python To PATH")
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv python3-pip
  ```
- **macOS:**
  ```bash
  brew install python@3.11
  ```

#### **2. Git (Optional, For Cloning)**

**Check If Installed:**

```powershell
git --version
```

**If Not Installed:**

- **Windows:** Download From [git-scm.com](https://git-scm.com/download/win)
- **Linux:** `sudo apt install git`
- **macOS:** `brew install git`

#### **3. Text Editor (Recommended)**

- **VS Code** (Best Python Support) — [Download](https://code.visualstudio.com/)
- **PyCharm Community** — [Download](https://www.jetbrains.com/pycharm/download/)
- **Sublime Text** — [Download](https://www.sublimetext.com/)

---

## Installation Steps

### **Step 1: Clone Or Download The Repository**

#### **Option A: Clone With Git (Recommended)**

```powershell
# Clone The Repository
git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git

# Navigate To Project Directory
cd AGRI-SENSE_GUARDIAN
```

#### **Option B: Download ZIP**

1. Go To [GitHub Repository](https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN)
2. Click **Code** → **Download ZIP**
3. Extract The ZIP File
4. Open Terminal/PowerShell In The Extracted Folder

---

### **Step 2: Create A Virtual Environment**

Virtual Environments Isolate Project Dependencies From Your System Python.

#### **Windows PowerShell**

```powershell
# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment
.\venv\Scripts\Activate.ps1

# If You Get "Execution Policy" Error, Run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then Try Activating Again
```

#### **Linux/macOS**

```bash
# Create Virtual Environment
python3 -m venv venv

# Activate Virtual Environment
source venv/bin/activate
```

**Verification:**

After Activation, Your Terminal Should Show `(venv)` At The Beginning:

```
(venv) PS C:\Users\...\AGRI-SENSE_GUARDIAN>
```

---

### **Step 3: Install Dependencies**

```powershell
# Upgrade pip First (Recommended)
pip install --upgrade pip

# Install All Dependencies
pip install -r Requirements.txt
```

**Expected Output:**

```
Successfully installed fastapi-0.115.0 uvicorn-0.30.0 pydantic-2.9.0 ...
```

**If You Encounter Errors:**

See [Troubleshooting](#troubleshooting) Section Below.

---

## API Key Configuration

### **Required API Keys**

| Service | Required? | Free Tier | Sign-Up Link |
|---------|-----------|-----------|--------------|
| **Google Gemini** | ✅ **REQUIRED** | 1500 Requests/Day | [Get Key](https://makersuite.google.com/app/apikey) |
| **OpenWeatherMap** | ✅ **REQUIRED** | 1000 Calls/Day | [Get Key](https://openweathermap.org/api) |
| **Copernicus CDS** | ⚠️ Optional | Unlimited | [Get Key](https://cds.climate.copernicus.eu/) |
| **Google Search** | ⚠️ Optional | 100 Queries/Day | [Get Key](https://developers.google.com/custom-search) |
| **Email SMTP** | ⚠️ Optional | N/A | Gmail/Outlook Account |

---

### **Step 4: Obtain API Keys**

#### **1. Google Gemini API Key (REQUIRED)**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign In With Google Account
3. Click **"Create API Key"**
4. Click **"Create API Key In New Project"** (Or Select Existing Project)
5. Copy The API Key (Starts With `AIza...`)

**Important:** Keep This Key Secret. Do Not Commit It To Git.

---

#### **2. OpenWeatherMap API Key (REQUIRED)**

1. Go To [OpenWeatherMap Signup](https://home.openweathermap.org/users/sign_up)
2. Create A Free Account
3. Verify Your Email
4. Go To [API Keys](https://home.openweathermap.org/api_keys)
5. Copy Your Default API Key (Or Create A New One)

**Activation Time:** May Take 10-30 Minutes For API Key To Activate.

---

#### **3. Copernicus CDS API Key (OPTIONAL)**

**Why Optional?** System Falls Back To NASA POWER Data If Unavailable.

**If You Want Better Data Quality:**

1. Register At [Copernicus CDS](https://cds.climate.copernicus.eu/user/register)
2. Verify Email And Accept Terms
3. Go To [Account Settings](https://cds.climate.copernicus.eu/user)
4. Copy **UID** And **API Key**
5. Format As: `UID:APIKEY` (E.g., `12345:abcdef123456`)

**Setup Instructions:**

```bash
# Linux/macOS
mkdir -p ~/.cdsapirc
echo "url: https://cds.climate.copernicus.eu/api/v2" > ~/.cdsapirc
echo "key: YOUR_UID:YOUR_API_KEY" >> ~/.cdsapirc

# Windows
# Create File: C:\Users\YourName\.cdsapirc
# Content:
url: https://cds.climate.copernicus.eu/api/v2
key: YOUR_UID:YOUR_API_KEY
```

---

#### **4. Google Custom Search API (OPTIONAL)**

**Why Optional?** VerifyAgent Uses This For Web Intelligence.

1. Go To [Google Cloud Console](https://console.cloud.google.com/)
2. Create New Project Or Select Existing
3. Enable **Custom Search API**
4. Create Credentials → **API Key**
5. Go To [Programmable Search Engine](https://programmablesearchengine.google.com/)
6. Create New Search Engine
7. Copy **Search Engine ID**

---

#### **5. Email SMTP (OPTIONAL)**

**Why Optional?** System Can Run Without Email, Just Won't Send Notifications.

**Gmail Setup:**

1. Enable 2-Factor Authentication On Your Gmail Account
2. Go To [App Passwords](https://myaccount.google.com/apppasswords)
3. Select **Mail** And **Other (Custom Name)** → "AgriSenseGuardian"
4. Copy The 16-Character App Password

**Outlook/Hotmail:**

- Use Your Regular Password (No App Password Needed)
- SMTP Host: `smtp-mail.outlook.com`
- Port: `587`

---

### **Step 5: Create .env File**

Create A File Named `.env` In The Project Root Directory:

#### **Windows PowerShell**

```powershell
# Create .env File
New-Item -Path .env -ItemType File

# Open In Notepad
notepad .env
```

#### **Linux/macOS**

```bash
# Create .env File
touch .env

# Open In Nano
nano .env
```

---

### **Step 6: Configure .env File**

Paste The Following Into Your `.env` File And Replace Placeholders:

```env
# ===== GOOGLE GEMINI AI (REQUIRED) =====
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ===== WEATHER DATA (REQUIRED) =====
OPENWEATHER_API_KEY=your_openweather_api_key_here

# ===== COPERNICUS CLIMATE DATA (OPTIONAL) =====
# Format: UID:APIKEY
COPERNICUS_API_KEY=12345:abcdef123456

# ===== GOOGLE SEARCH (OPTIONAL) =====
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# ===== EMAIL NOTIFICATIONS (OPTIONAL) =====
# Gmail Example:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SENDER_EMAIL=your_email@gmail.com
SENDER_NAME=AgriSenseGuardian

# Outlook Example:
# SMTP_HOST=smtp-mail.outlook.com
# SMTP_PORT=587
# SMTP_USER=your_email@outlook.com
# SMTP_PASSWORD=your_regular_password
# SENDER_EMAIL=your_email@outlook.com

# ===== APPLICATION SETTINGS =====
API_HOST=127.0.0.1
API_PORT=8000
LOG_LEVEL=INFO
START_A2A_ON_STARTUP=true

# ===== A2A AGENT PORTS =====
A2A_HOST=0.0.0.0
# (Ports Are Auto-Configured, No Need To Change)
```

**Save The File.**

**Security Note:** Never Commit `.env` To Git. It's Already In `.gitignore`.

---

## Running The Application

### **Step 7: Start The Application**

#### **Windows PowerShell**

```powershell
# Make Sure Virtual Environment Is Activated
# You Should See (venv) At The Start Of The Line

# Run The Application
python Main.py
```

#### **Linux/macOS**

```bash
# Make Sure Virtual Environment Is Activated
source venv/bin/activate

# Run The Application
python Main.py
```

---

### **Expected Output**

```
INFO:     Started Server Process [12345]
INFO:     Waiting For Application Startup.
INFO:     🚀 Bootstrapping A2A Agent Servers...
INFO:     Starting OrchestratorAgent Server On Port 9000...
INFO:     ✅ OrchestratorAgent Server Running On Port 9000
INFO:     Starting ForecastAgent Server On Port 9001...
INFO:     ✅ ForecastAgent Server Running On Port 9001
INFO:     Starting VerifyAgent Server On Port 9002...
INFO:     ✅ VerifyAgent Server Running On Port 9002
INFO:     Application Startup Complete.
INFO:     Uvicorn Running On http://127.0.0.1:8000 (Press CTRL+C To Quit)
```

**If You See This, The Application Is Running! 🎉**

---

### **Step 8: Access The Web UI**

1. Open Your Web Browser
2. Navigate To: **http://127.0.0.1:8000**
3. You Should See The AgriSenseGuardian Web Interface

---

## Verification & Testing

### **Test 1: Web UI Loads**

**Expected:** You See A Form With:
- Location Input Field
- Email Input Field
- Days Ahead Slider
- "Get Forecast" Button

---

### **Test 2: Submit A Test Request**

1. **Enter Location:** "Punjab, India"
2. **Enter Email:** your_email@example.com
3. **Days Ahead:** 30
4. **Click:** "Get Forecast"

**Expected Result (Within 5-10 Seconds):**

```json
{
  "Status": "Success",
  "RiskAssessment": {
    "Drought": "Medium",
    "Flood": "Low",
    "Heat": "Low",
    "Disease": "Medium",
    "Pest": "Low"
  },
  "ActionPlan": [
    "Monitor Soil Moisture Levels Daily",
    "Ensure Irrigation System Is Ready",
    "Apply Preventive Fungicide For Disease Risk"
  ],
  "EmailSent": true
}
```

---

### **Test 3: Check Health Endpoint**

**In Browser:**

Navigate To: **http://127.0.0.1:8000/health**

**Expected Response:**

```json
{
  "Status": "Healthy",
  "Message": "AgriSenseGuardian Is Running",
  "WebUI": "http://127.0.0.1:8000",
  "AgentsRunning": true
}
```

---

### **Test 4: Check Metrics Endpoint**

**In Browser:**

Navigate To: **http://127.0.0.1:8000/metrics**

**Expected:** Prometheus Metrics Output (Plain Text)

```
# HELP agent_execution_seconds Agent Execution Duration In Seconds
# TYPE agent_execution_seconds histogram
agent_execution_seconds_bucket{agent="ForecastAgent",le="0.1"} 0
...
```

---

## Troubleshooting

### **Problem: "ModuleNotFoundError: No Module Named 'fastapi'"**

**Cause:** Dependencies Not Installed

**Solution:**

```powershell
# Make Sure Virtual Environment Is Activated
# You Should See (venv) At The Start Of The Line

# Install Dependencies
pip install -r Requirements.txt
```

---

### **Problem: "Virtual Environment Activation Failed (Execution Policy)"**

**Windows Only — PowerShell Execution Policy Restriction**

**Solution:**

```powershell
# Allow Script Execution For Current User
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Confirm With "Y"

# Try Activating Again
.\venv\Scripts\Activate.ps1
```

---

### **Problem: "Port 8000 Already In Use"**

**Cause:** Another Application Is Using Port 8000

**Solution 1:** Stop The Other Application

**Solution 2:** Change Port In `.env`

```env
API_PORT=8080  # Or Any Other Free Port
```

Then Restart The Application And Access At `http://127.0.0.1:8080`

---

### **Problem: "OpenWeatherMap API Returns 401 Unauthorized"**

**Cause:** Invalid API Key Or Key Not Activated Yet

**Solution:**

1. Verify API Key In `.env` Matches Your OpenWeatherMap Account
2. Wait 10-30 Minutes For Key Activation
3. Test API Key Manually:

```powershell
# Windows PowerShell
$ApiKey = "your_api_key"
Invoke-WebRequest "https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid=$ApiKey"
```

If You Get `{"cod":"401"}`, Key Is Invalid Or Not Activated.

---

### **Problem: "No Module Named 'cdsapi'"**

**Cause:** Copernicus Optional Dependency Not Installed

**Solution 1:** Install cdsapi

```powershell
pip install cdsapi
```

**Solution 2:** Remove Copernicus API Key From `.env`

The System Will Automatically Fall Back To NASA POWER Data.

---

### **Problem: "Email Not Sending"**

**Cause:** SMTP Configuration Issue

**Debug Steps:**

1. **Check SMTP Settings In `.env`**
   - Gmail: Port 587, Host `smtp.gmail.com`
   - Outlook: Port 587, Host `smtp-mail.outlook.com`

2. **Verify App Password (Gmail)**
   - Must Use App Password, Not Regular Password
   - Enable 2FA First

3. **Test SMTP Manually:**

```python
# test_smtp.py
import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test Email")
msg["Subject"] = "Test"
msg["From"] = "your_email@gmail.com"
msg["To"] = "your_email@gmail.com"

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("your_email@gmail.com", "your_app_password")
    server.send_message(msg)
    print("Email Sent!")
```

---

### **Problem: "Agent Servers Not Starting"**

**Cause:** Port Conflicts Or Startup Errors

**Debug Steps:**

1. **Check Logs:**

```powershell
# Look For Error Messages In Terminal
# Agents Should Show "✅ Running On Port XXXX"
```

2. **Manually Test Agent Server:**

```powershell
# Start Orchestrator Manually
cd Agents
python OrchestratorServer.py
```

If It Fails, Error Message Will Show Root Cause.

---

### **Problem: "Python Version Too Old"**

**Error:** `SyntaxError: Invalid Syntax` Or `Type Hints Not Supported`

**Cause:** Python < 3.11

**Solution:**

```powershell
# Check Version
python --version

# Must Be 3.11.0 Or Higher
# If Not, Install Python 3.11+ And Recreate Virtual Environment
```

---

## Production Deployment

### **Option 1: Docker Deployment (Recommended)**

**Create `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "Main.py"]
```

**Build And Run:**

```bash
# Build Image
docker build -t agrisense-guardian .

# Run Container
docker run -p 8000:8000 --env-file .env agrisense-guardian
```

---

### **Option 2: Google Cloud Run**

```bash
# Install Google Cloud SDK
# Then Deploy:

gcloud run deploy agrisense-guardian \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### **Option 3: Traditional Server (Linux)**

**Using Systemd Service:**

Create `/etc/systemd/system/agrisense.service`:

```ini
[Unit]
Description=AgriSenseGuardian Multi-Agent System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/agrisense
Environment="PATH=/opt/agrisense/venv/bin"
ExecStart=/opt/agrisense/venv/bin/python Main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Start Service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable agrisense
sudo systemctl start agrisense
```

---

## FAQ

### **Q: Do I Need All API Keys To Run The Application?**

**A:** No. Only Google Gemini And OpenWeatherMap Are Required.

- **Copernicus:** Optional, Falls Back To NASA POWER
- **Google Search:** Optional, VerifyAgent Uses Limited Validation
- **Email SMTP:** Optional, Just Won't Send Notifications

---

### **Q: How Much Do The API Keys Cost?**

**A:** All Free Tiers Are Sufficient For Development/Demo:

- **Google Gemini:** 1500 Requests/Day (Free)
- **OpenWeatherMap:** 1000 Calls/Day (Free)
- **Copernicus:** Unlimited (Free)
- **Google Search:** 100 Queries/Day (Free)

---

### **Q: Can I Use This For Production With Real Farmers?**

**A:** Yes, But Upgrade To Paid API Plans:

- **Google Gemini:** Pay-As-You-Go Pricing
- **OpenWeatherMap:** Professional Plan (~$40/Month)

Also Consider:
- Database-Backed Sessions (PostgreSQL)
- Load Balancer For Multiple Instances
- Monitoring With Grafana/Prometheus

---

### **Q: How Do I Update To The Latest Version?**

```bash
# Pull Latest Code
git pull origin main

# Update Dependencies
pip install --upgrade -r Requirements.txt

# Restart Application
python Main.py
```

---

### **Q: Where Are Logs Stored?**

**Development:** Console Output Only

**Production:** Configure File Logging In `Utils/Logger.py`

```python
# Add File Handler
FileHandler = logging.FileHandler("app.log")
Logger.addHandler(FileHandler)
```

---

### **Q: Can I Run This On A Raspberry Pi?**

**A:** Technically Yes, But Performance Will Be Limited.

**Requirements:**
- Raspberry Pi 4 (4GB+ RAM)
- Python 3.11 (Build From Source)
- Expect Slower Response Times

---

## Next Steps

### **✅ You're All Set! Now:**

1. **Test The Application** — Submit A Few Forecast Requests
2. **Read The Documentation:**
   - [README.md](README.md) — Project Overview
   - [ARCHITECTURE.md](ARCHITECTURE.md) — Technical Deep Dive
   - [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) — Demo Script
3. **Explore The Code:**
   - `Agents/` — Multi-Agent System
   - `Tools/` — Data Collection Tools
   - `Services/` — Session, Task, Health Services
4. **Contribute:**
   - See [CONTRIBUTING.md](CONTRIBUTING.md) For Guidelines
5. **Star The Repository** ⭐ If You Find This Useful!

---

## Support

### **Need Help?**

- **GitHub Issues:** [Report Bug](https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN/issues)
- **Email:** your-email@example.com
- **Documentation:** See [README.md](README.md)

---

<div align="center">

**🚀 Setup Complete! Welcome To AgriSenseGuardian!**

**🌾 Start Protecting Farms With AI-Powered Intelligence**

---

**📚 Related Documentation**

[README.md](README.md) | [ARCHITECTURE.md](ARCHITECTURE.md) | [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) | [CHANGELOG.md](CHANGELOG.md)

</div>
