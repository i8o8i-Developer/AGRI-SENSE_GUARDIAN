// ============================================================================
// 🌾 AgriSenseGuardian — Modern UI Controller
// Handles Form Submission, Multi-Language, Theme, API Communication
// ============================================================================

'use strict';

// ===== CONFIGURATION =====
const CONFIG = {
  API_ENDPOINT: '/forecast',
  TASK: {
    START: '/tasks/start',
    STATUS: (id) => `/tasks/${id}/status`,
    PAUSE: (id) => `/tasks/${id}/pause`,
    RESUME: (id) => `/tasks/${id}/resume`,
    CANCEL: (id) => `/tasks/${id}/cancel`,
    POLL_INTERVAL: 2000
  },
  LOADING_STEPS: [
    '📡 Fetching Weather, Satellite & Copernicus Data In Parallel...',
    '🛰️ Analyzing Multi-Source Imagery With AI...',
    '🤖 Running Concurrent Risk Assessment Agents...',
    '🌐 Cross-Validating With Web Search & Open Sources...',
    '🧠 Optimizing Context & Refining Loop Iterations...',
    '📋 Generating Action Plan With Local Resources...',
    '✅ Finalizing Recommendations With Email Delivery...'
  ],
  STEP_INTERVAL: 2000, 
  QUICK_LOCATIONS: [
    { name: 'Mumbai', emoji: '🏙️', full: 'Mumbai, Maharashtra, India' },
    { name: 'Delhi', emoji: '🏛️', full: 'Delhi, India' },
    { name: 'Pune', emoji: '🌆', full: 'Pune, Maharashtra, India' },
    { name: 'Bangalore', emoji: '💼', full: 'Bangalore, Karnataka, India' },
    { name: 'Chennai', emoji: '🌴', full: 'Chennai, Tamil Nadu, India' },
    { name: 'Hyderabad', emoji: '🏰', full: 'Hyderabad, Telangana, India' }
  ]
};

// ===== TRANSLATIONS =====
const TRANSLATIONS = {
  en: {
    title: 'AgriSenseGuardian',
    subtitle: 'AI Agricultural Intelligence',
    formTitle: 'Get Your Farm Forecast',
    formDescription: 'Enter Your Location And Contact Details For AI-Powered Insights With Web Search Verification, Configurable Thresholds, And Long-Running Task Support',
    locationLabel: 'Your Location',
    locationPlaceholder: 'Enter City, Village, Or Coordinates (e.g., Mumbai, Maharashtra)',
    phoneLabel: 'Mobile Number',
    phonePlaceholder: '+91 9876543210',
    emailLabel: 'Email Address',
    emailPlaceholder: 'Farmer@example.com',
    daysLabel: 'Forecast Period',
    daysOption7: '7 Days (1 Week)',
    daysOption14: '14 Days (2 Weeks)',
    daysOption30: '30 Days (1 Month)',
    queryLabel: 'What Do You Want To Know?',
    queryPlaceholder: 'e.g., Should I Plant Tomatoes? What Are The Drought Risks?',
    submitButton: 'Get Forecast',
    loadingTitle: 'Multi-Agent Analysis In Progress (Parallel Execution, Web Search, Context Optimization)...',
    helpline: 'Need Help? Call Kisan Call Centre: 1800-180-1551 (24/7 Free)'
  },
  hi: {
    title: 'कृषि सेंस गार्डियन',
    subtitle: 'एआई कृषि बुद्धिमत्ता',
    formTitle: 'अपनी फसल का पूर्वानुमान प्राप्त करें',
    formDescription: 'एआई-संचालित अंतर्दृष्टि, वेब खोज सत्यापन, और दीर्घकालिक कार्य समर्थन के लिए अपना स्थान और विवरण दर्ज करें',
    locationLabel: 'आपका स्थान',
    locationPlaceholder: 'शहर, गाँव, या निर्देशांक दर्ज करें',
    phoneLabel: 'मोबाइल नंबर',
    phonePlaceholder: '+91 9876543210',
    emailLabel: 'ईमेल पता',
    emailPlaceholder: 'किसान@example.com',
    daysLabel: 'पूर्वानुमान अवधि',
    daysOption7: '7 दिन (1 सप्ताह)',
    daysOption14: '14 दिन (2 सप्ताह)',
    daysOption30: '30 दिन (1 महीना)',
    queryLabel: 'आप क्या जानना चाहते हैं?',
    queryPlaceholder: 'जैसे, क्या मुझे टमाटर लगाना चाहिए? सूखे के जोखिम क्या हैं?',
    submitButton: 'पूर्वानुमान प्राप्त करें',
    loadingTitle: 'बहु-एजेंट विश्लेषण प्रगति में (समानांतर निष्पादन, वेब खोज, संदर्भ अनुकूलन)...',
    helpline: 'मदद चाहिए? किसान कॉल सेंटर पर कॉल करें: 1800-180-1551 (24/7 मुफ्त)'
  }
};

// ===== STATE =====
let CurrentLang = 'en';
let LoadingStepInterval = null;
let CurrentTaskId = null;
let TaskPollInterval = null;

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
  console.log('🌾 AgriSenseGuardian Initialized');
  InitializeUI();
  SetupEventListeners();
  PopulateQuickLocations();
});

// ===== UI INITIALIZATION =====
function InitializeUI() {
  InitializeTheme();
  UpdateLanguage();
}

// ===== THEME MANAGEMENT =====
function InitializeTheme() {
  const SavedTheme = localStorage.getItem('AgriSense_Theme') || 'dark';
  document.body.classList.toggle('light', SavedTheme === 'light');
  UpdateThemeIcon();
}

function ToggleTheme() {
  document.body.classList.toggle('light');
  const NewTheme = document.body.classList.contains('light') ? 'light' : 'dark';
  localStorage.setItem('AgriSense_Theme', NewTheme);
  UpdateThemeIcon();
}

function UpdateThemeIcon() {
  const ThemeBtn = document.getElementById('ThemeToggle');
  if (ThemeBtn) {
    ThemeBtn.textContent = document.body.classList.contains('light') ? '🌙' : '☀️';
  }
}

// ===== LANGUAGE MANAGEMENT =====
function SwitchLanguage(Lang) {
  CurrentLang = Lang;
  
  // Update Active Button
  document.querySelectorAll('.LangBtn').forEach(Btn => {
    Btn.classList.toggle('active', Btn.dataset.lang === Lang);
  });
  
  UpdateLanguage();
}

function UpdateLanguage() {
  const T = TRANSLATIONS[CurrentLang];
  
  document.querySelectorAll('[data-i18n]').forEach(Element => {
    const Key = Element.dataset.i18n;
    if (T[Key]) {
      if (Element.tagName === 'INPUT' || Element.tagName === 'TEXTAREA') {
        Element.placeholder = T[Key];
      } else {
        Element.textContent = T[Key];
      }
    }
  });
}

// ===== QUICK LOCATIONS =====
function PopulateQuickLocations() {
  const Container = document.getElementById('QuickLocations');
  if (!Container) return;
  
  Container.innerHTML = '';
  
  CONFIG.QUICK_LOCATIONS.forEach(Loc => {
    const Btn = document.createElement('button');
    Btn.type = 'button';
    Btn.className = 'QuickBtn';
    Btn.innerHTML = `<span>${Loc.emoji}</span><span>${Loc.name}</span>`;
    Btn.addEventListener('click', () => {
      document.getElementById('Location').value = Loc.full;
    });
    Container.appendChild(Btn);
  });
}

// ===== EVENT LISTENERS =====
function SetupEventListeners() {
  // Language Buttons
  document.querySelectorAll('.LangBtn').forEach(Btn => {
    Btn.addEventListener('click', () => SwitchLanguage(Btn.dataset.lang));
  });
  
  // Theme Toggle
  const ThemeToggle = document.getElementById('ThemeToggle');
  if (ThemeToggle) {
    ThemeToggle.addEventListener('click', ToggleTheme);
  }
  
  // Form Submit
  const Form = document.getElementById('ForecastForm');
  if (Form) {
    Form.addEventListener('submit', HandleFormSubmit);
  }

  // Background Task Start
  const BgBtn = document.getElementById('StartBackground');
  if (BgBtn) {
    BgBtn.addEventListener('click', StartBackgroundTask);
  }

  // Task Controls
  const PauseBtn = document.getElementById('TaskPause');
  const ResumeBtn = document.getElementById('TaskResume');
  const CancelBtn = document.getElementById('TaskCancel');
  if (PauseBtn) PauseBtn.addEventListener('click', PauseTask);
  if (ResumeBtn) ResumeBtn.addEventListener('click', ResumeTask);
  if (CancelBtn) CancelBtn.addEventListener('click', CancelTask);
  
  // Phone Formatting
  const PhoneInput = document.getElementById('Phone');
  if (PhoneInput) {
    PhoneInput.addEventListener('input', FormatPhoneNumber);
  }
}

// ===== PHONE FORMATTING =====
function FormatPhoneNumber(Event) {
  let Value = Event.target.value.replace(/\D/g, '');
  
  // Auto-Add +91 Prefix For Indian Numbers
  if (Value.length > 0 && !Value.startsWith('91')) {
    if (Value.length === 10) {
      Value = '91' + Value;
    }
  }
  
  // Format as +91 XXXXX XXXXX
  if (Value.startsWith('91') && Value.length >= 2) {
    const Formatted = '+91 ' + Value.slice(2, 7) + (Value.length > 7 ? ' ' + Value.slice(7, 12) : '');
    Event.target.value = Formatted.trim();
  } else {
    Event.target.value = Value;
  }
}

// ===== FORM SUBMISSION =====
async function HandleFormSubmit(Event) {
  Event.preventDefault();
  
  // Collect Form Data
  const FormData = {
    Location: document.getElementById('Location').value.trim(),
    // FarmerPhone Removed - SMS Is Deprecated; Email Is Primary Contact
    FarmerEmail: document.getElementById('Email').value.trim(),
    DaysAhead: parseInt(document.getElementById('Days').value),
    UserQuery: document.getElementById('Query').value.trim() || 'What Are The Agricultural Risks For My Farm?'
  };
  
  // Validation
  if (!FormData.Location || !FormData.FarmerEmail) {
    ShowError('Please Fill In All Required Fields (Location, Email)');
    return;
  }
  
  // Email Validation
  if (!ValidateEmail(FormData.FarmerEmail)) {
    ShowError('Please Enter A Valid Email Address');
    return;
  }
  
  console.log('📤 Submitting Forecast Request:', FormData);
  
  // Show Loading
  ShowLoading();
  
  try {
    // Call API
    const Response = await fetch(CONFIG.API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(FormData)
    });
    
    if (!Response.ok) {
      throw new Error(`API Error: ${Response.status} ${Response.statusText}`);
    }
    
    const Data = await Response.json();
    console.log('📥 Received Response:', Data);
    
    // Normalize Response
    const NormalizedData = NormalizeResponseData(Data);
    
    // Hide Loading, Show Results
    HideLoading();
    DisplayResults(NormalizedData);
    
  } catch (Error) {
    console.error('❌ Request Failed:', Error);
    HideLoading();
    ShowError(Error.message || 'Failed To Generate Forecast. Please Try Again.');
  }
}

// ===== BACKGROUND TASK FLOW =====
async function StartBackgroundTask() {
  // Collect Form Data
  const Payload = {
    Location: document.getElementById('Location').value.trim(),
    FarmerEmail: document.getElementById('Email').value.trim(),
    DaysAhead: parseInt(document.getElementById('Days').value),
    UserQuery: document.getElementById('Query').value.trim() || 'What Are The Agricultural Risks For My Farm?',
    ConfidenceThreshold: parseInt(document.getElementById('ConfidenceThreshold')?.value || 75),
    MaxIterations: parseInt(document.getElementById('MaxIterations')?.value || 2)
  };

  if (!Payload.Location || !Payload.FarmerEmail) {
    ShowError('Please Fill In All Required Fields (Location, Email)');
    return;
  }
  if (!ValidateEmail(Payload.FarmerEmail)) {
    ShowError('Please Enter A Valid Email Address');
    return;
  }

  try {
    const Resp = await fetch(CONFIG.TASK.START, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(Payload)
    });
    if (!Resp.ok) throw new Error(`Task Start Failed: ${Resp.status}`);
    const Data = await Resp.json();
    if (!Data.TaskId) throw new Error('No TaskId Returned');

    CurrentTaskId = Data.TaskId;
    ShowTaskPanel({ id: CurrentTaskId, state: 'Running', message: 'Task started. Polling Status...' });
    StartTaskPolling();
  } catch (err) {
    console.error('❌ Background Start Failed :', err);
    ShowError(err.message || 'Failed To Start Background Task');
  }
}

function StartTaskPolling() {
  StopTaskPolling();
  TaskPollInterval = setInterval(PollTaskStatus, CONFIG.TASK.POLL_INTERVAL);
  PollTaskStatus();
}

function StopTaskPolling() {
  if (TaskPollInterval) {
    clearInterval(TaskPollInterval);
    TaskPollInterval = null;
  }
}

async function PollTaskStatus() {
  if (!CurrentTaskId) return;
  try {
    const Resp = await fetch(CONFIG.TASK.STATUS(CurrentTaskId));
    if (!Resp.ok) throw new Error(`Status Failed: ${Resp.status}`);
    const Data = await Resp.json();
    const Task = Data.Task || {};
    UpdateTaskPanel(Task);

    const state = (Task.State || '').toLowerCase();
    if (state === 'completed') {
      StopTaskPolling();
      const Result = Task.Result || null;
      if (Result) {
        const Normalized = NormalizeResponseData(Result);
        DisplayResults(Normalized);
      }
      AppendTaskLog('✅ Task Completed. Results Displayed.');
    } else if (state === 'error') {
      StopTaskPolling();
      AppendTaskLog(`❌ Error: ${Task.Error || 'Unknown error'}`);
      ShowError(Task.Error || 'Task Failed');
    } else if (state === 'cancelled') {
      StopTaskPolling();
      AppendTaskLog('🛑 Task Cancelled.');
    }
  } catch (err) {
    console.error('❌ Polling Error:', err);
    AppendTaskLog(`⚠️ Polling Failed: ${err.message}`);
  }
}

async function PauseTask() {
  if (!CurrentTaskId) return;
  try {
    const Resp = await fetch(CONFIG.TASK.PAUSE(CurrentTaskId), { method: 'POST' });
    const Data = await Resp.json();
    AppendTaskLog(`⏸️ Paused: ${Data.State || 'Paused'}`);
    PollTaskStatus();
  } catch (err) { AppendTaskLog(`⚠️ Pause Failed: ${err.message}`); }
}

async function ResumeTask() {
  if (!CurrentTaskId) return;
  try {
    const Resp = await fetch(CONFIG.TASK.RESUME(CurrentTaskId), { method: 'POST' });
    const Data = await Resp.json();
    AppendTaskLog(`▶️ Resumed: ${Data.State || 'Running'}`);
    PollTaskStatus();
  } catch (err) { AppendTaskLog(`⚠️ Resume Failed: ${err.message}`); }
}

async function CancelTask() {
  if (!CurrentTaskId) return;
  try {
    const Resp = await fetch(CONFIG.TASK.CANCEL(CurrentTaskId), { method: 'POST' });
    const Data = await Resp.json();
    AppendTaskLog(`🛑 Cancelled: ${Data.State || 'Cancelled'}`);
    PollTaskStatus();
  } catch (err) { AppendTaskLog(`⚠️ Cancel Failed: ${err.message}`); }
}

function ShowTaskPanel({ id, state, message }) {
  const Panel = document.getElementById('TaskPanel');
  Panel.classList.remove('Hidden');
  document.getElementById('TaskId').textContent = id;
  document.getElementById('TaskState').textContent = state || '—';
  const Log = document.getElementById('TaskLog');
  Log.innerHTML = '';
  if (message) AppendTaskLog(message);
}

function UpdateTaskPanel(Task) {
  document.getElementById('TaskId').textContent = Task.Id || CurrentTaskId || '—';
  document.getElementById('TaskState').textContent = Task.State || '—';
}

function AppendTaskLog(msg) {
  const Log = document.getElementById('TaskLog');
  const p = document.createElement('div');
  p.className = 'TaskLogLine';
  const ts = new Date().toLocaleTimeString();
  p.textContent = `[${ts}] ${msg}`;
  Log.appendChild(p);
}

// ===== EMAIL VALIDATION =====
function ValidateEmail(Email) {
  const Regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return Regex.test(Email);
}

// ===== RESPONSE NORMALIZATION =====
function NormalizeResponseData(Data) {
  console.log('🔍 Normalizing Response Data:', Data);
  
  if (!Data) {
    console.warn('⚠️ No Data Received');
    return Data;
  }
  
  const Normalized = JSON.parse(JSON.stringify(Data));
  
  // Log The Raw Structure
  console.log('📦 ForecastResults:', Data.ForecastResults);
  console.log('📦 ActionPlan:', Data.ActionPlan);
  console.log('📦 VerificationResults:', Data.VerificationResults);
  
  // Normalize Action Plan
  const AP = Data.ActionPlan || {};
  Normalized.ActionPlan = {
    P1: AP.P1 || AP.P1_CriticalActions || AP.P1_Critical || [],
    P2: AP.P2 || AP.P2_ImportantActions || AP.P2_Important || [],
    P3: AP.P3 || AP.P3_MonitoringActions || AP.P3_Monitoring || [],
    EmailDeliveryStatus: AP.EmailDeliveryStatus || AP.EmailStatus || {},
    UserQuestion: AP.UserQuestion || Data.UserQuery || '',
    ImmediateAction: AP.ImmediateAction || '',
    ThisWeekAction: AP.ThisWeekAction || '',
    UserQueryResponse: AP.UserQueryResponse || ''
  };
  
  // Ensure Forecast Results
  if (!Normalized.ForecastResults) {
    Normalized.ForecastResults = Data.ForecastResults || {};
  }
  
  console.log('✅ Normalized Data:', Normalized);
  return Normalized;
}

// ===== LOADING STATE =====
function ShowLoading() {
  document.getElementById('InputSection').classList.add('Hidden');
  
  const LoadingEl = document.getElementById('Loading');
  LoadingEl.classList.add('active');
  
  // Animate Loading Steps
  const StepEl = document.getElementById('LoadingStep');
  let CurrentStep = 0;
  
  LoadingStepInterval = setInterval(() => {
    if (CurrentStep < CONFIG.LOADING_STEPS.length) {
      StepEl.textContent = CONFIG.LOADING_STEPS[CurrentStep];
      CurrentStep++;
    } else {
      clearInterval(LoadingStepInterval);
    }
  }, CONFIG.STEP_INTERVAL);
}

function HideLoading() {
  if (LoadingStepInterval) {
    clearInterval(LoadingStepInterval);
    LoadingStepInterval = null;
  }
  
  const LoadingEl = document.getElementById('Loading');
  LoadingEl.classList.remove('active');
}

// ===== DISPLAY RESULTS =====
function DisplayResults(Data) {
  console.log('🎨 Displaying Results:', Data);
  
  const ResultsEl = document.getElementById('ResultsSection');
  ResultsEl.classList.add('active');
  
  // Scroll To Results
  ResultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  
  // Update Header with safe defaults
  document.getElementById('ResultLocation').textContent = Data.Location || 'Your Farm';
  document.getElementById('ResultDate').textContent = new Date().toLocaleDateString();
  document.getElementById('ResultDays').textContent = (Data.ForecastResults?.ForecastHorizonDays || Data.ForecastResults?.forecastHorizonDays || 30);
  
  // Display Components With Safe Defaults
  const forecastResults = Data.ForecastResults || {};
  const actionPlan = Data.ActionPlan || {};
  
  console.log('📊 Risk Categories:', forecastResults.RiskCategories || forecastResults.riskCategories);
  console.log('📋 Action Plan P1:', actionPlan.P1);
  console.log('📋 Action Plan P2:', actionPlan.P2);
  console.log('📋 Action Plan P3:', actionPlan.P3);
  
  DisplayRiskOverview(forecastResults.RiskCategories || forecastResults.riskCategories || {});
  DisplayDataSources(forecastResults.DataSources || forecastResults.dataSources || []);
  DisplayQuestionAnswer(actionPlan);
  DisplayActionPlan(actionPlan);
  DisplayEmailStatus(actionPlan.EmailDeliveryStatus || actionPlan.emailDeliveryStatus || {});
}

// ===== RISK OVERVIEW =====
function DisplayRiskOverview(Risks) {
  const Container = document.getElementById('RiskOverview');
  Container.innerHTML = '';
  
  const RiskMapping = {
    'DroughtRisk': { name: 'Drought Risk', icon: '☀️' },
    'FloodRisk': { name: 'Flood Risk', icon: '💧' },
    'PestOutbreakRisk': { name: 'Pest Risk', icon: '🐛' },
    'DiseaseRisk': { name: 'Disease Risk', icon: '🦠' },
    'HeatStressRisk': { name: 'Heat Stress', icon: '🌡️' },
    'SoilErosionRisk': { name: 'Soil Erosion', icon: '⛰️' },
    'NutrientLeachingRisk': { name: 'Nutrient Leaching', icon: '🧪' },
    'ColdStressRisk': { name: 'Cold Stress', icon: '❄️' },
    'VegetationStressRisk': { name: 'Vegetation Stress', icon: '🌿' }
  };
  
  Object.entries(Risks).forEach(([Key, Risk]) => {
    const Info = RiskMapping[Key];
    if (!Info) return;
    
    const Level = (Risk.Level || 'Low').toLowerCase();
    
    const Card = document.createElement('div');
    Card.className = `RiskCard ${Level}`;
    Card.innerHTML = `
      <div class="RiskCardHeader">
        <div class="RiskName">${Info.icon} ${Info.name}</div>
        <div class="RiskLevel ${Level}">${Risk.Level || 'Low'}</div>
      </div>
      <div class="RiskConfidence">Confidence: ${Risk.Confidence || 0}%</div>
    `;
    Container.appendChild(Card);
  });
}

// ===== DATA SOURCES =====
function DisplayDataSources(Sources) {
  const Container = document.getElementById('DataSources');
  Container.innerHTML = '';
  
  (Sources || []).forEach(Source => {
    const Chip = document.createElement('span');
    Chip.className = 'DataChip';
    Chip.innerHTML = `<span>✓</span><span>${Source}</span>`;
    Container.appendChild(Chip);
  });
}

// ===== ACTION PLAN =====
function DisplayActionPlan(ActionPlan) {
  const Priorities = ['P1', 'P2', 'P3'];
  const Labels = {
    'P1': '🚨 Critical - Do Immediately',
    'P2': '⚠️ Important - This Week',
    'P3': '📋 Monitor - Ongoing'
  };
  
  Priorities.forEach(Priority => {
    const Container = document.getElementById(`Actions${Priority}`);
    if (!Container) return;
    
    const Title = Container.previousElementSibling;
    if (Title) {
      Title.innerHTML = Labels[Priority];
    }
    
    Container.innerHTML = '';
    
    const Actions = ActionPlan[Priority] || [];
    if (Actions.length === 0) {
      const Li = document.createElement('li');
      Li.className = 'ActionItem';
      Li.textContent = 'No Actions Required At This Priority Level';
      Container.appendChild(Li);
      return;
    }
    
    Actions.forEach(Action => {
      const Li = document.createElement('li');
      Li.className = `ActionItem priority-${Priority === 'P1' ? 'high' : Priority === 'P2' ? 'medium' : 'low'}`;
      let raw = Action;
      if (typeof Action !== 'string') {
        raw = Action.Action || Action.title || JSON.stringify(Action);
      }
      
      // Render Markdown Instead Of Plain Text Conversion
      const contentDiv = document.createElement('div');
      contentDiv.className = 'markdown-content';
      contentDiv.innerHTML = RenderMarkdown(raw);
      Li.appendChild(contentDiv);
      
      // Append Enrichment Metadata If Present
      if (typeof Action === 'object') {
        const metaParts = [];
        if (Action.Deadline) metaParts.push(`<span class="meta dead">🕒 ${Action.Deadline}</span>`);
        if (Action.Resources && Action.Resources.length) metaParts.push(`<span class="meta res">🔧 ${Action.Resources.join(', ')}</span>`);
        if (Action.CostEstimateINR !== undefined) metaParts.push(`<span class="meta cost">₹${Action.CostEstimateINR}</span>`);
        if (Action.ExpectedOutcome) metaParts.push(`<span class="meta outcome">🎯 ${Action.ExpectedOutcome}</span>`);
        
        if (metaParts.length) {
          const MetaDiv = document.createElement('div');
          MetaDiv.className = 'ActionMeta';
          MetaDiv.innerHTML = metaParts.join(' ');
          Li.appendChild(MetaDiv);
        }
      }
      Container.appendChild(Li);
    });
  });
}

// ===== MARKDOWN RENDERING UTILITY =====
function RenderMarkdown(text) {
  if (!text) return '—';
  
  // Configure Marked Options For Better Rendering
  if (typeof marked !== 'undefined') {
    marked.setOptions({
      breaks: true,
      gfm: true,
      headerIds: false,
      mangle: false
    });
    
    try {
      return marked.parse(text);
    } catch (e) {
      console.error('Markdown Parsing Error:', e);
      return text.replace(/\n/g, '<br>');
    }
  }
  
  // Fallback If Marked Is Not Loaded
  return text.replace(/\n/g, '<br>');
}

// ===== QUESTION & ANSWER SECTION =====
function DisplayQuestionAnswer(ActionPlan) {
  const Box = document.getElementById('QuestionAnswerBox');
  if (!Box) return;
  const question = ActionPlan.UserQuestion || '';
  const response = ActionPlan.UserQueryResponse || '';
  if (!question && !response) {
    Box.style.display = 'none';
    return;
  }
  document.getElementById('FarmerQuestion').textContent = question || '—';
  
  // Render markdown for LLM response
  const responseElement = document.getElementById('UserQueryResponse');
  responseElement.innerHTML = RenderMarkdown(response);
  responseElement.classList.add('markdown-content');
  
  Box.style.display = 'block';
}

// ===== EMAIL STATUS =====
function DisplayEmailStatus(Status) {
  const Container = document.getElementById('EmailStatus');
  if (!Container) return;
  
  Container.innerHTML = '';
  const statusCode = (Status.Status || '').toLowerCase();

  if (statusCode === 'success') {
    const Box = document.createElement('div');
    Box.className = 'InfoBox success';
    Box.innerHTML = `
      <div class="info-header">
        <span class="info-icon">✅</span>
        <strong>Email Delivered</strong>
      </div>
      <div class="info-content">
        <div class="info-row">
          <span class="info-label">Sent To:</span>
          <span class="info-value">${Status.EmailRecipient || 'Provided Address'}</span>
        </div>
        <div class="info-message">${Status.Message || 'Email Notification Sent Successfully'}</div>
      </div>
    `;
    Container.appendChild(Box);
  } else if (statusCode === 'skipped') {
    const Box = document.createElement('div');
    Box.className = 'InfoBox info';
    Box.innerHTML = `
      <div class="info-header">
        <span class="info-icon">ℹ️</span>
        <strong>Email Skipped</strong>
      </div>
      <div class="info-content">
        <div class="info-message">${Status.Reason || 'No Email Address Provided'}</div>
      </div>
    `;
    Container.appendChild(Box);
  } else if (statusCode === 'error') {
    const Box = document.createElement('div');
    Box.className = 'InfoBox error';
    Box.innerHTML = `
      <div class="info-header">
        <span class="info-icon">⚠️</span>
        <strong>Email Delivery Failed</strong>
      </div>
      <div class="info-content">
        <div class="info-message">${Status.Message || 'Unable To Send Email Notification. Please Check Your Email Address.'}</div>
      </div>
    `;
    Container.appendChild(Box);
  }
}

// ===== ERROR DISPLAY =====
function ShowError(Message) {
  const FormCard = document.getElementById('FormCard');
  const ErrorBox = document.createElement('div');
  ErrorBox.className = 'InfoBox error mt-4';
  ErrorBox.innerHTML = `
    <strong>❌ Error</strong><br>
    ${Message}
  `;
  
  // Remove Existing Error
  const ExistingError = FormCard.querySelector('.InfoBox.error');
  if (ExistingError) ExistingError.remove();
  
  // Add New Error
  FormCard.appendChild(ErrorBox);
  
  // Auto-Remove After 5s
  setTimeout(() => ErrorBox.remove(), 5000);
}

// ===== RESET FORM =====
function ResetForm() {
  document.getElementById('ForecastForm').reset();
  document.getElementById('ResultsSection').classList.remove('active');
  document.getElementById('InputSection').classList.remove('Hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== EXPORT FOR GLOBAL ACCESS =====
window.ResetForm = ResetForm;
window.resetForm = ResetForm; // Lowercase Alias For HTML Onclick

console.log('✅ AgriSenseGuardian UI Ready');
