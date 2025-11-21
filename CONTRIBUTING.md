# 🤝 Contributing To AgriSenseGuardian

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     CONTRIBUTION GUIDELINES                               ║
║              Help Us Build The Future Of Agricultural AI                  ║
║                    Welcome To The Community!                              ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## 🌾 Welcome Contributors!

Thank You For Your Interest In Contributing To AgriSenseGuardian! This Project Aims To Empower **150 Million Farmers** With AI-Driven Agricultural Intelligence. Every Contribution — Whether Code, Documentation, Bug Reports, Or Feature Ideas — Helps Make A Real-World Impact.

---

## 📜 Code Of Conduct

### **Our Pledge**

We Are Committed To Making Participation In This Project A Harassment-Free Experience For Everyone, Regardless Of:
- Age, Body Size, Disability, Ethnicity
- Gender Identity And Expression
- Level Of Experience
- Nationality, Personal Appearance
- Race, Religion, Or Sexual Identity And Orientation

### **Our Standards**

**Positive Behavior Includes:**
- ✅ Using Welcoming And Inclusive Language
- ✅ Respecting Differing Viewpoints And Experiences
- ✅ Gracefully Accepting Constructive Criticism
- ✅ Focusing On What's Best For The Community
- ✅ Showing Empathy Towards Others

**Unacceptable Behavior Includes:**
- ❌ Trolling, Insulting/Derogatory Comments, Personal Attacks
- ❌ Public Or Private Harassment
- ❌ Publishing Others' Private Information Without Permission
- ❌ Other Conduct Reasonably Considered Inappropriate

### **Enforcement**

Project Maintainers Will Review And Respond To All Code Of Conduct Violations. Contact: **[Repository Owner]**

---

## 🎯 How Can I Contribute?

### **1. 🐛 Report Bugs**

Found A Bug? Help Us Fix It!

**Before Submitting:**
- ✅ Check [Existing Issues](https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN/issues) To Avoid Duplicates
- ✅ Verify The Bug In The Latest Version

**Create A Bug Report:**
1. Go To [Issues](https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN/issues/new)
2. Use The "Bug Report" Template
3. Include:
   - Clear Description Of The Problem
   - Steps To Reproduce
   - Expected Vs Actual Behavior
   - Environment Details (OS, Python Version, etc.)
   - Error Messages/Logs
   - Screenshots (If Applicable)

**Example:**
```markdown
**Bug:** ForecastAgent Crashes On Invalid Location Input

**Steps To Reproduce:**
1. Start OrchestratorAgent Server
2. Send Request With Location: "!@#$%"
3. Observe Error

**Expected:** Validation Error With Helpful Message
**Actual:** Server Crash With Stack Trace

**Environment:**
- OS: Windows 11
- Python: 3.11.5
- AgriSenseGuardian: v1.0.0
```

---

### **2. 💡 Suggest Features**

Have An Idea To Improve AgriSenseGuardian?

**Submit A Feature Request:**
1. Go To [Feature Request Template](FEATURE_REQUEST.md)
2. Fill Out All Required Sections
3. Submit As GitHub Issue With Label `enhancement`

**What Makes A Good Feature Request:**
- ✅ Solves A Real Problem For Farmers Or Users
- ✅ Aligns With Project Goals (Sustainability, Accessibility)
- ✅ Includes Use Cases And Expected Benefits
- ✅ Considers Technical Feasibility

---

### **3. 📝 Improve Documentation**

Documentation Is As Important As Code!

**Documentation Improvements:**
- Fix Typos Or Grammatical Errors
- Clarify Confusing Sections
- Add Examples Or Tutorials
- Translate Documentation (Future)
- Create Video Tutorials

**Documentation Files:**
- [README.md](README.md) — Project Overview
- [ARCHITECTURE.md](ARCHITECTURE.md) — Technical Architecture
- [SETUP_GUIDE.md](SETUP_GUIDE.md) — Installation Guide
- [Docs/](Docs/) — Advanced Documentation

**How To Contribute:**
1. Fork The Repository
2. Edit Documentation Files
3. Submit Pull Request With Clear Description

---

### **4. 💻 Contribute Code**

Ready To Write Code?

**Areas Where We Need Help:**
- 🔧 **Bug Fixes** — Fix Open Issues
- ✨ **New Features** — Implement Requested Features
- 🧪 **Tests** — Improve Test Coverage
- ⚡ **Performance** — Optimize Algorithms
- 🌐 **Integrations** — Add New Data Sources/Tools
- 🎨 **UI/UX** — Improve Web Interface

**Before You Start:**
1. Check [Open Issues](https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN/issues)
2. Comment On The Issue To Claim It
3. Wait For Maintainer Approval
4. Follow Development Workflow (See Below)

---

## 🚀 Getting Started

### **Prerequisites**

Ensure You Have:
- ✅ Python 3.11 Or Higher
- ✅ Git Installed
- ✅ GitHub Account
- ✅ Code Editor (VS Code Recommended)

### **Setup Development Environment**

**1. Fork The Repository**

Click "Fork" On [GitHub Repository](https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN)

**2. Clone Your Fork**

```powershell
# Clone Repository
git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git
cd AGRI-SENSE_GUARDIAN

# Add Upstream Remote
git remote add upstream https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git
```

**3. Install Dependencies**

```powershell
# Create Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r Requirements.txt

# Install Development Dependencies (Future)
# pip install -r Requirements-dev.txt
```

**4. Configure Environment**

```powershell
# Copy Example Environment File
Copy-Item .env.example .env

# Edit .env With Your API Keys
notepad .env
```

**5. Run Tests (Future)**

```powershell
# Run All Tests
pytest

# Run With Coverage
pytest --cov=. --cov-report=html
```

---

## 🔄 Development Workflow

### **Step 1: Create A Branch**

**Branch Naming Convention:**
- `feature/description` — New Features
- `fix/description` — Bug Fixes
- `docs/description` — Documentation Changes
- `refactor/description` — Code Refactoring
- `test/description` — Test Additions

**Example:**
```powershell
# Create Feature Branch
git checkout -b feature/add-multi-language-support

# Create Bug Fix Branch
git checkout -b fix/forecast-agent-validation
```

---

### **Step 2: Make Changes**

**Follow Coding Standards:**
- ✅ Use **PascalCase** For All Naming (See [DEVELOPMENT_RATIONALE.md](DEVELOPMENT_RATIONALE.md))
- ✅ Add Docstrings To All Functions/Classes
- ✅ Include Type Hints For Parameters/Returns
- ✅ Add Inline Comments For Complex Logic
- ✅ Keep Functions Focused And Small (< 50 Lines)

**Example:**

```python
async def ValidateLocationInput(Location: str) -> bool:
    """
    Validate User-Provided Location Input For Geographic Queries.
    
    Ensures Location String Contains Only Valid Characters And Meets
    Length Requirements Before Passing To Geocoding APIs.
    
    Args:
        Location: User Input Location String (City, State, Coordinates)
        
    Returns:
        bool: True If Valid, False Otherwise
        
    Raises:
        ValueError: If Location Contains Dangerous Characters
    """
    # Prevent SQL Injection And XSS Attacks
    if re.search(r'[<>"\';\\]', Location):
        raise ValueError("Invalid Characters In Location Input")
    
    # Ensure Reasonable Length
    if len(Location) < 2 or len(Location) > 200:
        return False
    
    return True
```

---

### **Step 3: Test Your Changes**

**Manual Testing:**
```powershell
# Start Application
python Main.py

# Test Your Feature
# (Send Requests, Check Logs, Verify Behavior)
```

**Automated Testing (Future):**
```powershell
# Run Unit Tests
pytest tests/unittests/

# Run Integration Tests
pytest tests/integration/

# Check Code Coverage
pytest --cov=.
```

---

### **Step 4: Commit Changes**

**Commit Message Format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` — New Feature
- `fix` — Bug Fix
- `docs` — Documentation Changes
- `style` — Code Formatting (No Logic Change)
- `refactor` — Code Refactoring
- `test` — Adding Tests
- `chore` — Build/Config Changes

**Example:**

```powershell
git add .
git commit -m "feat(ForecastAgent): Add Multi-Source Data Validation

- Implement Input Validation For All Weather APIs
- Add Circuit Breaker For API Failure Handling
- Include Unit Tests For Edge Cases

Closes #42"
```

---

### **Step 5: Push To GitHub**

```powershell
# Push Branch To Your Fork
git push origin feature/add-multi-language-support
```

---

### **Step 6: Create Pull Request**

**1. Go To GitHub Repository**

Navigate To: `https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN`

**2. Click "Pull Request"**

Click "Compare & Pull Request" Button

**3. Fill Out PR Template**

```markdown
## Description
Brief Description Of Changes

## Type Of Change
- [ ] Bug Fix
- [x] New Feature
- [ ] Documentation Update
- [ ] Performance Improvement

## Related Issues
Closes #42

## Testing
- [x] Manual Testing Completed
- [x] All Existing Tests Pass
- [x] Added New Tests For This Feature

## Screenshots (If Applicable)
[Attach Screenshots]

## Checklist
- [x] Code Follows PascalCase Convention
- [x] Added Docstrings And Type Hints
- [x] Updated Documentation (If Needed)
- [x] No Breaking Changes
```

**4. Request Review**

Maintainers Will Review Your PR Within 7 Days

---

## 📐 Coding Standards

### **1. PascalCase Convention**

**AgriSenseGuardian Uses PascalCase Everywhere:**

```python
# ✅ Correct (PascalCase)
def FetchWeatherData(Location: str, DaysAhead: int) -> Dict[str, Any]:
    WeatherData = {}
    ApiKey = os.getenv('OPENWEATHER_API_KEY')
    return WeatherData

# ❌ Incorrect (snake_case)
def fetch_weather_data(location: str, days_ahead: int) -> dict:
    weather_data = {}
    api_key = os.getenv('OPENWEATHER_API_KEY')
    return weather_data
```

**Why PascalCase?** See [DEVELOPMENT_RATIONALE.md](DEVELOPMENT_RATIONALE.md)

---

### **2. Docstrings (Required)**

**Every Function/Class Must Have Docstrings:**

```python
def CalculateDroughtRisk(
    PrecipitationRatio: float,
    SoilMoisture: float,
    CropType: str
) -> str:
    """
    Calculate Drought Risk Level Based On FAO Guidelines.
    
    Implements FAO-56 Methodology For Drought Assessment Using
    Precipitation Patterns, Soil Moisture Levels, And Crop-Specific
    Water Requirements.
    
    Args:
        PrecipitationRatio: Current/Historical Precipitation Ratio (0.0-2.0)
        SoilMoisture: Volumetric Water Content (0.0-1.0)
        CropType: Crop Type String ('Rice', 'Wheat', 'Cotton')
        
    Returns:
        str: Risk Level ('High', 'Medium', 'Low')
        
    Raises:
        ValueError: If Parameters Are Out Of Valid Range
        
    References:
        Allen Et Al. (1998) "Crop Evapotranspiration", FAO-56
    """
    # Implementation...
```

---

### **3. Type Hints (Required)**

**All Parameters And Returns Must Have Type Hints:**

```python
# ✅ Correct
async def ProcessForecast(
    Location: str,
    DaysAhead: int,
    Session: SessionContext
) -> Dict[str, Any]:
    pass

# ❌ Incorrect (No Type Hints)
async def ProcessForecast(Location, DaysAhead, Session):
    pass
```

---

### **4. Code Comments**

**Add Inline Comments For Complex Logic:**

```python
# Calculate Weighted Average With Bayesian Confidence
# Based On Source Reliability Studies (NASA: 40%, Weather: 30%)
FusedValue = (
    NasaValue * 0.40 +
    WeatherValue * 0.30 +
    SoilValue * 0.20 +
    HistoricalValue * 0.10
)
```

---

### **5. Error Handling**

**Always Handle Errors Gracefully:**

```python
try:
    Data = await FetchFromAPI(Url)
    return Data
except aiohttp.ClientError as ApiError:
    Logger.error(f"API Request Failed: {ApiError}")
    # Fallback To Secondary Source
    return await FetchFromFallbackAPI(Url)
except Exception as UnknownError:
    Logger.critical(f"Unexpected Error: {UnknownError}")
    raise
```

---

### **6. File Structure**

**Organize Code By Functionality:**

```
AGRI-SENSE_GUARDIAN/
├── Agents/           # Agent Implementation
├── Tools/            # Tool Implementations
├── Services/         # Shared Services
├── Utils/            # Utility Functions
├── Config/           # Configuration
├── Tests/            # Test Files (Future)
└── Docs/             # Documentation
```

---

## 📤 Submitting Changes

### **Pull Request Checklist**

Before Submitting, Ensure:

- [ ] **Code Quality**
  - [ ] Follows PascalCase Convention
  - [ ] All Functions Have Docstrings
  - [ ] Type Hints Added
  - [ ] Inline Comments For Complex Logic

- [ ] **Testing**
  - [ ] Manual Testing Completed
  - [ ] No Regressions In Existing Features
  - [ ] Edge Cases Considered

- [ ] **Documentation**
  - [ ] Updated README (If Feature Affects Usage)
  - [ ] Updated ARCHITECTURE (If Design Changes)
  - [ ] Added Code Comments

- [ ] **Git Hygiene**
  - [ ] Descriptive Commit Messages
  - [ ] Branch Named Correctly
  - [ ] No Merge Conflicts

- [ ] **No Breaking Changes**
  - [ ] Backward Compatible
  - [ ] Deprecation Warnings (If Needed)

---

## 🌍 Community Guidelines

### **Be Respectful**
- Value Diverse Perspectives
- Assume Good Intentions
- Provide Constructive Feedback

### **Be Collaborative**
- Share Knowledge Freely
- Help New Contributors
- Celebrate Successes Together

### **Be Patient**
- Reviews Take Time
- Questions Are Welcome
- Learning Is Encouraged

---

## 📞 Getting Help

**Need Assistance?**

- 💬 **GitHub Discussions** — Ask Questions, Share Ideas
- 🐛 **GitHub Issues** — Report Bugs, Request Features
- 📧 **Email** — [Contact Maintainers]
- 📚 **Documentation** — [Docs/INDEX.md](Docs/INDEX.md)

---

## 🎉 Recognition

### **Contributors**

All Contributors Will Be:
- ✅ Listed In [CHANGELOG.md](CHANGELOG.md)
- ✅ Mentioned In Release Notes
- ✅ Credited In Documentation

### **Types Of Contributions**

We Recognize:
- 💻 **Code Contributors** — Feature Development, Bug Fixes
- 📝 **Documentation Contributors** — Docs, Tutorials, Translations
- 🐛 **Bug Reporters** — Quality Assurance, Testing
- 💡 **Idea Contributors** — Feature Suggestions, Feedback
- 🎨 **Design Contributors** — UI/UX, Graphics, Branding

---

## 📚 Additional Resources

- **[README.md](README.md)** — Project Overview
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — Technical Architecture
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** — Installation Guide
- **[DEVELOPMENT_RATIONALE.md](DEVELOPMENT_RATIONALE.md)** — Design Decisions
- **[FEATURE_REQUEST.md](FEATURE_REQUEST.md)** — Feature Request Template
- **[LICENSE](LICENSE)** — Apache 2.0 License
- **[Docs/INDEX.md](Docs/INDEX.md)** — Documentation Index

---

<div align="center">

**🤝 Together, We Build The Future Of Agriculture**

**Thank You For Contributing To AgriSenseGuardian! 🌾**

---

**Every Contribution Matters — From Code To Documentation To Ideas**

**Join Us In Empowering 150 Million Farmers With AI Technology**

</div>
