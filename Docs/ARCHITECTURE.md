# 🏗️ AgriSenseGuardian — System Architecture Documentation

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    AGRISENSEGUARDIAN ARCHITECTURE                         ║
║              Multi-Agent Agricultural Intelligence Platform               ║
║                         Technical Deep Dive                               ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## System Overview

### **High-Level System Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE LAYER                           │
│                                                                             │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         │
│  │   Web UI     │         │   REST API   │         │   WebSocket  │         │
│  │  (HTML/JS)   │──────▶│   (FastAPI)  │───────▶│   (Future)   │         │
│  └──────────────┘         └──────────────┘         └──────────────┘         │
│         │                         │                         │               │
└─────────┼─────────────────────────┼─────────────────────────┼───────────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────────┐
│                         APPLICATION ORCHESTRATION LAYER                    │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      OrchestratorAgent (Port 9000)                   │  │
│  │                                                                      │  │
│  │  Responsibilities:                                                   │  │
│  │  • Request Routing & Task Coordination                               │  │
│  │  • Session State Management                                          │  │
│  │  • Memory Bank Integration                                           │  │
│  │  • Quality Assurance (Loop Control)                                  │  │
│  │  • Error Handling & Recovery                                         │  │
│  │  • Observability Integration                                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└───────────────────────┬──────────────────┬──────────────────┬──────────────┘
                        │                  │                  │
                        ▼                  ▼                  ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                          SPECIALIZED AGENT LAYER                          │
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │  ForecastAgent   │  │   VerifyAgent    │  │  PlannerAgent    │         │
│  │   (Port 9001)    │  │   (Port 9002)    │  │   (Port 9003)    │         │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤         │
│  │ • Data           │  │ • Cross-         │  │ • Action Plan    │         │
│  │   Collection     │  │   Validation     │  │   Generation     │         │
│  │ • Risk           │  │ • Confidence     │  │ • Email          │         │
│  │   Calculation    │  │   Scoring        │  │   Notification   │         │
│  │ • Multi-Source   │  │ • Web Search     │  │ • Prioritization │         │
│  │   Fusion         │  │   Verification   │  │ • Resource       │         │
│  │ • Parallel       │  │ • Anomaly        │  │   Mapping        │         │
│  │   Tool Exec      │  │   Detection      │  │ • Summarization  │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                           │
└───────────────────────────────┬───────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                              TOOL LAYER                                   │
│                                                                           │
│  ┌─────────────────────── ENVIRONMENTAL DATA TOOLS ────────────────────┐  │
│  │                                                                     │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │
│  │  │ WeatherTool  │  │SatelliteTool │  │CopernicusTool│               │  │
│  │  │(OpenWeather) │  │  (NASA API)  │  │  (ESA CDS)   │               │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │  │
│  │                                                                     │  │
│  │  ┌──────────────┐                                                   │  │
│  │  │ (SoilGrids)  │                                                   │  │
│  │  └──────────────┘                                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌──────────────────── WEB INTELLIGENCE TOOLS ────────────────────────┐   │
│  │                                                                    │   │
│  │  ┌──────────────┐                                                  │   │
│  │  │GoogleSearch  │                                                  │   │
│  │  │    Tool      │                                                  │   │
│  │  └──────────────┘                                                  │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────── COMMUNICATION TOOLS ─────────────────────────────┐  │
│  │                                                                     │  │
│  │  ┌──────────────┐  ┌───────────────┐                                │  │
│  │  │EmailNotify   │  │SMSNotification│                                │  │
│  │  └──────────────┘  └───────────────┘                                │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌────────────────────── COMPUTE TOOLS ────────────────────────────────┐  │
│  │                                                                     │  │
│  │  ┌──────────────┐                                                   │  │
│  │  │CodeExecution │                                                   │  │
│  │  │    Tool      │                                                   │  │
│  │  └──────────────┘                                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                         CROSS-CUTTING SERVICES                            │
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Session    │  │    Memory    │  │Observability │  │    Task      │   │
│  │  Management  │  │    Bank      │  │   (Logs,     │  │  Manager     │   │
│  │              │  │              │  │ Traces, etc) │  │(Pause/Resume)│   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL DATA SOURCES                              │
│                                                                           │
│  🌦️ OpenWeatherMap  │  🛰️ NASA POWER  │  🌍 Copernicus CDS              │
│  🌐 Google Search   │  📧 SMTP Email   │  🗺️ ISRIC SoilGrids             │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Architectural Principles

### **1. Separation Of Concerns**

Each Component Has A Single, Well-Defined Responsibility:

- **Agents** — Intelligence & Decision-Making
- **Tools** — Data Collection & External Integrations
- **Services** — Cross-Cutting Concerns (Sessions, Memory, Tasks)
- **Utils** — Shared Utilities (Logging, Observability)

### **2. Modularity**

All Components Are Independently Deployable And Replaceable:

```python
# Agent Interface
class BaseAgent:
    async def Run(self, Input: Dict[str, Any]) -> Dict[str, Any]:
        """Standard Agent Execution Interface"""
        pass

# Tool Interface
async def BaseTool(Context: ToolContext) -> Dict[str, Any]:
    """Standard Tool Interface"""
    pass
```

### **3. Asynchronous First**

All I/O Operations Use Python's `async/await` For Maximum Concurrency:

```python
# Parallel Tool Execution
Tasks = [
    WeatherTool(Location, DaysAhead),
    SatelliteTool(Location, DaysAhead),
    CopernicusTool(Location, DaysAhead)
]
Results = await asyncio.gather(*Tasks)
```

### **4. Fail-Safe Design**

Every External Call Has Graceful Fallback Mechanisms:

```python
try:
    Data = await FetchFromAPI()
except Exception as E:
    Logger.warning(f"API Failed, Using Fallback: {E}")
    Data = FallbackData()
```

### **5. Observability By Default**

All Operations Are Instrumented With Logging, Tracing, And Metrics:

```python
@record_agent_duration("ForecastAgent")
async def Run():
    Logger.info("Starting Forecast")
    with use_span("ForecastAgent.DataCollection"):
        # Operation Code
        pass
```

---

## Layer Architecture

### **Layer 1: Presentation Layer**

**Responsibilities:**
- User Interface (Web UI)
- API Request/Response Handling
- Input Validation
- Output Formatting

**Technologies:**
- FastAPI (Web Framework)
- Jinja2 (Template Engine)
- Pydantic (Data Validation)
- HTML/CSS/JavaScript (Frontend)

**Key Files:**
- `Main.py` — Application Entry Point
- `Templates/index.html` — Web UI
- `Static/` — CSS/JS Assets

### **Layer 2: Orchestration Layer**

**Responsibilities:**
- Multi-Agent Coordination
- Workflow Management
- Session State Tracking
- Quality Assurance (Loop Control)
- Error Recovery

**Technologies:**
- Google ADK (Agent Framework)
- A2A Protocol (Agent Communication)
- Gemini 2.5 Flash Lite (LLM)

**Key Files:**
- `Agents/OrchestratorAgent.py` — Master Coordinator
- `Agents/OrchestratorServer.py` — A2A HTTP Server

### **Layer 3: Agent Layer**

**Responsibilities:**
- Specialized Task Execution
- Domain-Specific Intelligence
- Tool Orchestration
- Result Synthesis

**Technologies:**
- Google ADK Agents
- Async Python
- Type Hints (Pydantic)

**Key Files:**
- `Agents/ForecastAgent.py` — Data Collection & Risk Analysis
- `Agents/VerifyAgent.py` — Validation & Confidence Scoring
- `Agents/PlannerAgent.py` — Action Planning & Communication

### **Layer 4: Tool Layer**

**Responsibilities:**
- External API Integration
- Data Collection
- Data Transformation
- Error Handling

**Technologies:**
- HTTP Clients (aiohttp, httpx)
- API SDKs (cdsapi, geopy)
- MCP Protocol (Partial)

**Key Files:**
- `Tools/WeatherTool.py`
- `Tools/SatelliteTool.py`
- `Tools/CopernicusTool.py`
- `Tools/SoilTestTool.py`
- `Tools/GoogleSearchTool.py`
- `Tools/EmailNotificationTool.py`
- `Tools/CodeExecutionTool.py`

### **Layer 5: Service Layer**

**Responsibilities:**
- Session Management
- Memory Persistence
- Task Orchestration
- Health Monitoring

**Technologies:**
- ADK InMemorySessionService
- ADK InMemoryMemoryService
- AsyncIO Task Management

**Key Files:**
- `Services/AgentBootstrap.py` — Agent Server Lifecycle
- `Services/TaskManager.py` — Long-Running Task Management
- `Services/HealthService.py` — System Health Checks
- `Utils/SessionManager.py` — Session & Memory
- `Utils/Observability.py` — Logging, Tracing, Metrics

---

## Multi-Agent System Design

### **Agent Hierarchy**

```
┌─────────────────────────────────────────────────────────────────┐
│                    OrchestratorAgent                            │
│                   (Master Coordinator)                          │
│                                                                 │
│  Role: Strategic Planning & Quality Assurance                   │
│  Pattern: Sequential + Loop                                     │
│  LLM: Gemini 2.5 Flash Lite (Temperature: 0.1)                  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ ForecastAgent │ │  VerifyAgent  │ │ PlannerAgent  │
├───────────────┤ ├───────────────┤ ├───────────────┤
│ Role:         │ │ Role:         │ │ Role:         │
│ Data          │ │ Quality       │ │ Action        │
│ Collection &  │ │ Assurance &   │ │ Planning &    │
│ Risk Analysis │ │ Validation    │ │ Communication │
│               │ │               │ │               │
│ Pattern:      │ │ Pattern:      │ │ Pattern:      │
│ Parallel      │ │ Sequential    │ │ Sequential    │
│               │ │               │ │               │
│ LLM:          │ │ LLM:          │ │ LLM:          │
│ Gemini 2.5    │ │ Gemini 2.5    │ │ Gemini 2.5    │
│ Flash Lite    │ │ Flash Lite    │ │ Flash Lite    │
│ (Temp: 0.3)   │ │ (Temp: 0.2)   │ │ (Temp: 0.4)   │
└───────────────┘ └───────────────┘ └───────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                Tools Layer
```

### **Agent Communication Patterns**

#### **1. Sequential Pattern (Default)**

```
User Request
     │
     ▼
OrchestratorAgent
     │
     ├──▶ ForecastAgent ──▶ Risk Data
     │         │
     │         ▼
     ├──▶ VerifyAgent ──▶ Confidence Score
     │         │
     │         ▼
     └──▶ PlannerAgent ──▶ Action Plan
           │
           ▼
      Final Response
```

**Advantages:**
- ✅ Guaranteed Execution Order
- ✅ Data Dependencies Preserved
- ✅ Quality Control At Each Step
- ✅ Clear Error Propagation

**Implementation:**

```python
async def Execute(self, UserQuery: str):
    # Step 1: Forecast
    ForecastResult = await self.ForecastAgent.Run()
    
    # Step 2: Verify
    VerifyResult = await self.VerifyAgent.Run(ForecastResult)
    
    # Step 3: Plan
    PlannerResult = await self.PlannerAgent.Run(ForecastResult, VerifyResult)
    
    return PlannerResult
```

#### **2. Parallel Pattern (Tool Execution)**

```
ForecastAgent
     │
     ├──────┬──────┬──────┬──────┐
     │      │      │      │      │
     ▼      ▼      ▼      ▼      ▼
 Weather Satellite Copernicus Soil Google
  Tool     Tool      Tool      Tool Search
     │      │      │      │      │
     └──────┴──────┴──────┴──────┘
              │
              ▼
        Risk Calculation
```

**Advantages:**
- ✅ 3-4x Faster Than Sequential
- ✅ Maximum Resource Utilization
- ✅ Independent Tool Failures Don't Block Others

**Implementation:**

```python
async def Run(self, Location: str):
    # Create Parallel Tasks
    Tasks = [
        WeatherTool(Location, DaysAhead),
        SatelliteTool(Location, DaysAhead),
        CopernicusTool(Location, DaysAhead),
        SoilTestTool(Location)
    ]
    
    # Execute In Parallel
    Results = await asyncio.gather(*Tasks, return_exceptions=True)
    
    # Combine Results
    WeatherData, SatelliteData, CopernicusData, SoilData = Results
    
    return self.ComputeRisk(WeatherData, SatelliteData, CopernicusData, SoilData)
```

#### **3. Loop Pattern (Quality Assurance)**

```
OrchestratorAgent
     │
     ├──▶ ForecastAgent ──▶ Risk Data
     │         │
     │         ▼
     ├──▶ VerifyAgent ──▶ Confidence Score
     │         │
     │         ├──▶ Confidence < 0.7? ──▶ YES ──▶ Loop Back To Forecast
     │         │                                   (Max 3 Iterations)
     │         ├──▶ Confidence >= 0.7? ──▶ NO
     │         │
     │         ▼
     └──▶ PlannerAgent ──▶ Action Plan
```

**Advantages:**
- ✅ Automatic Quality Improvement
- ✅ Handles Low-Confidence Results
- ✅ Prevents Poor Recommendations

**Implementation:**

```python
MaxIterations = 3
Iteration = 0
Confidence = 0.0

while Confidence < 0.7 and Iteration < MaxIterations:
    # Forecast
    ForecastResult = await self.ForecastAgent.Run(
        feedback=VerifyResult.get("Issues", []) if Iteration > 0 else []
    )
    
    # Verify
    VerifyResult = await self.VerifyAgent.Run(ForecastResult)
    Confidence = VerifyResult.get("Confidence", 0.0)
    
    Logger.info(f"Iteration {Iteration + 1}: Confidence = {Confidence}")
    Iteration += 1

if Confidence < 0.7:
    Logger.warning("Max Iterations Reached, Proceeding With Partial Results")
```

---

## Agent Communication (A2A Protocol)

### **A2A Protocol Overview**

A2A (Agent-To-Agent) Is Google's Standard Protocol For Multi-Agent Systems:

```
┌─────────────────────────────────────────────────────────────┐
│                   A2A PROTOCOL STACK                        │
├─────────────────────────────────────────────────────────────┤
│  Application Layer    │  JSON-Based Messages                │
├─────────────────────────────────────────────────────────────┤
│  Transport Layer      │  HTTP/HTTPS                         │
├─────────────────────────────────────────────────────────────┤
│  Network Layer        │  TCP/IP (Localhost Or Remote)       │
└─────────────────────────────────────────────────────────────┘
```

### **Message Format**

#### **Request Message**

```json
{
  "type": "task",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent": "ForecastAgent",
  "method": "Run",
  "parameters": {
    "Location": "Punjab, India",
    "DaysAhead": 30,
    "UserQuery": "What Are The Risks For My Farm?"
  },
  "context": {
    "session_id": "session-abc-123",
    "user_id": "farmer@example.com",
    "trace_id": "trace-xyz-789"
  },
  "metadata": {
    "timestamp": "2024-12-15T10:30:00Z",
    "client_version": "1.0.0"
  }
}
```

#### **Response Message**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "RiskAssessment": {
      "Drought": "High",
      "Flood": "Low",
      "Heat": "Medium",
      "Disease": "Medium",
      "Pest": "Low"
    },
    "Confidence": 0.85,
    "DataSources": ["OpenWeatherMap", "NASA", "Copernicus"]
  },
  "metadata": {
    "execution_time_ms": 320,
    "tools_called": ["WeatherTool", "SatelliteTool", "CopernicusTool"],
    "agent_version": "1.0.0",
    "model": "gemini-2.5-flash-lite"
  },
  "errors": []
}
```

#### **Error Response**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "error",
  "result": null,
  "errors": [
    {
      "code": "TOOL_FAILURE",
      "message": "WeatherTool API Timeout",
      "tool": "WeatherTool",
      "recoverable": true
    }
  ],
  "metadata": {
    "execution_time_ms": 5000,
    "retry_count": 3
  }
}
```

### **Agent Server Implementation**

Each Agent Runs As A Separate HTTP Server:

```python
# Agents/ForecastAgentServer.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Agents.ForecastAgent import ForecastAgent

app = FastAPI(title="ForecastAgent Server", version="1.0.0")
AgentInstance = ForecastAgent()

class TaskRequest(BaseModel):
    task_id: str
    parameters: dict
    context: dict

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: dict
    metadata: dict

@app.post("/execute", response_model=TaskResponse)
async def Execute(request: TaskRequest):
    """A2A Endpoint For ForecastAgent Execution"""
    try:
        # Extract Parameters
        Location = request.parameters.get("Location")
        DaysAhead = request.parameters.get("DaysAhead", 30)
        
        # Execute Agent
        StartTime = time.time()
        Result = await AgentInstance.Run(Location, DaysAhead)
        ExecutionTime = (time.time() - StartTime) * 1000
        
        # Return Response
        return TaskResponse(
            task_id=request.task_id,
            status="completed",
            result=Result,
            metadata={
                "execution_time_ms": ExecutionTime,
                "agent_version": "1.0.0"
            }
        )
    except Exception as E:
        raise HTTPException(status_code=500, detail=str(E))

@app.get("/health")
async def Health():
    """Health Check Endpoint"""
    return {"status": "healthy", "agent": "ForecastAgent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)
```

### **Agent Discovery & Bootstrapping**

```python
# Services/AgentBootstrap.py
class AgentBootstrap:
    async def StartAllAgents(self):
        """Launch All A2A Agent Servers"""
        
        # Start Orchestrator Server (Port 9000)
        OrchestratorProcess = await self.StartAgentServer(
            module="Agents.OrchestratorServer",
            port=9000
        )
        
        # Start Forecast Server (Port 9001)
        ForecastProcess = await self.StartAgentServer(
            module="Agents.ForecastAgentServer",
            port=9001
        )
        
        # Start Verify Server (Port 9002)
        VerifyProcess = await self.StartAgentServer(
            module="Agents.VerifyAgentServer",
            port=9002
        )
        
        Logger.info("✅ All A2A Agent Servers Running")
```

---

## Tool Architecture

### **Tool Interface Design**

All Tools Follow A Unified Interface For Consistency:

```python
# Tool Interface Signature
async def ToolName(
    # Required Parameters
    Location: str,
    
    # Optional Parameters
    DaysAhead: int = 30,
    
    # ADK Tool Context
    ToolContextInstance: ToolContext
) -> Dict[str, Any]:
    """
    Tool Description And Purpose.
    
    Args:
        Location: Geographic Location String
        DaysAhead: Forecast Horizon
        ToolContextInstance: ADK Tool Context For State Management
        
    Returns:
        Structured Dict With:
        - Status: "Success" | "Error"
        - Data: Tool-Specific Output
        - Metadata: Source, Timestamp, Confidence
    """
    pass
```

### **Tool Categories & Implementations**

#### **1. Environmental Data Tools**

##### **WeatherTool**

```python
async def WeatherTool(Location: str, DaysAhead: int, ToolContext: ToolContext) -> Dict[str, Any]:
    """
    Fetch Weather Forecasts From OpenWeatherMap API.
    
    API: OpenWeatherMap OneCall API 3.0
    Coverage: Global
    Resolution: 3-Hour Forecast, 30-Day Horizon
    """
    
    # Geocode Location
    Lat, Lon = await GeocodeLocation(Location)
    
    # Fetch Weather Data
    ApiKey = os.getenv("OPENWEATHER_API_KEY")
    Url = f"https://api.openweathermap.org/data/3.0/onecall?lat={Lat}&lon={Lon}&appid={ApiKey}"
    
    async with aiohttp.ClientSession() as Session:
        async with Session.get(Url) as Response:
            Data = await Response.json()
    
    # Process Data
    return {
        "Status": "Success",
        "Temperature": {
            "Max": Data["daily"][0]["temp"]["max"],
            "Min": Data["daily"][0]["temp"]["min"]
        },
        "Precipitation": {
            "Total": sum(day["rain"] for day in Data["daily"][:DaysAhead]),
            "Probability": Data["daily"][0]["pop"]
        },
        "Humidity": {
            "Average": sum(day["humidity"] for day in Data["daily"][:DaysAhead]) / DaysAhead
        },
        "Source": "OpenWeatherMap",
        "Timestamp": datetime.now().isoformat()
    }
```

##### **SatelliteTool (NASA POWER)**

```python
async def GetSatelliteData(Location: str, DaysBack: int, ToolContext: ToolContext) -> Dict[str, Any]:
    """
    Retrieve Satellite-Based Agroclimatology From NASA POWER.
    
    API: NASA POWER API
    Datasets: MERRA-2, MODIS
    Parameters: Solar Radiation, ET, Temperature, Precipitation
    """
    
    Lat, Lon = await GeocodeLocation(Location)
    
    # NASA POWER API Endpoint
    Url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
    Params = {
        "latitude": Lat,
        "longitude": Lon,
        "start": (datetime.now() - timedelta(days=DaysBack)).strftime("%Y%m%d"),
        "end": datetime.now().strftime("%Y%m%d"),
        "community": "AG",
        "parameters": "T2M,PRECTOT,ALLSKY_SFC_SW_DWN,EVPTRNS",
        "format": "JSON"
    }
    
    async with aiohttp.ClientSession() as Session:
        async with Session.get(Url, params=Params) as Response:
            Data = await Response.json()
    
    return {
        "Status": "Success",
        "SolarRadiation": {
            "Average": sum(Data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"].values()) / DaysBack
        },
        "Evapotranspiration": {
            "Average": sum(Data["properties"]["parameter"]["EVPTRNS"].values()) / DaysBack
        },
        "Temperature": {
            "Average": sum(Data["properties"]["parameter"]["T2M"].values()) / DaysBack
        },
        "Precipitation": {
            "Total": sum(Data["properties"]["parameter"]["PRECTOT"].values())
        },
        "Source": "NASA POWER",
        "Timestamp": datetime.now().isoformat()
    }
```

##### **CopernicusTool (ESA Copernicus CDS)**

```python
async def CopernicusTool(Location: str, DaysBack: int, ToolContext: ToolContext) -> Dict[str, Any]:
    """
    Access European Space Agency Climate Data Store.
    
    API: Copernicus CDS API
    Datasets: ERA5-Land, Sentinel-2
    Parameters: Soil Moisture, NDVI, LST, ET
    """
    
    # Check For Copernicus API Credentials
    ApiKey = os.getenv("COPERNICUS_API_KEY")
    if not ApiKey or ':' not in ApiKey:
        # Fallback To NASA POWER
        return await FallbackFromNASAPower(Location, DaysBack)
    
    import cdsapi
    Client = cdsapi.Client()
    
    Lat, Lon = await GeocodeLocation(Location)
    
    # Fetch ERA5-Land Data
    Client.retrieve(
        'reanalysis-era5-land',
        {
            'variable': ['volumetric_soil_water_layer_1', 'leaf_area_index_high_vegetation'],
            'year': datetime.now().year,
            'month': datetime.now().month,
            'day': [str(i) for i in range(1, datetime.now().day + 1)],
            'time': '12:00',
            'area': [Lat+0.1, Lon-0.1, Lat-0.1, Lon+0.1],
            'format': 'netcdf'
        },
        'download.nc'
    )
    
    # Process NetCDF File
    import xarray as xr
    Dataset = xr.open_dataset('download.nc')
    
    return {
        "Status": "Success",
        "SoilMoisture": {
            "Level": float(Dataset['swvl1'].mean().values),
            "Unit": "m³/m³"
        },
        "VegetationHealth": {
            "NDVI": float(Dataset['lai_hv'].mean().values),
            "Interpretation": "Healthy" if Dataset['lai_hv'].mean().values > 3 else "Stressed"
        },
        "Source": "Copernicus CDS",
        "Timestamp": datetime.now().isoformat()
    }
```

##### **SoilTestTool (ISRIC SoilGrids)**

```python
async def SoilTestTool(Location: str, ToolContext: ToolContext) -> Dict[str, Any]:
    """
    Get Soil Properties From Global Soil Database.
    
    API: ISRIC SoilGrids REST API
    Resolution: 250m
    Depth: 0-200cm (7 Layers)
    """
    
    Lat, Lon = await GeocodeLocation(Location)
    
    # SoilGrids API Endpoint
    Url = f"https://rest.isric.org/soilgrids/v2.0/properties/query"
    Params = {
        "lat": Lat,
        "lon": Lon,
        "property": ["phh2o", "clay", "sand", "nitrogen", "ocd"],
        "depth": ["0-5cm", "5-15cm"],
        "value": "mean"
    }
    
    async with aiohttp.ClientSession() as Session:
        async with Session.get(Url, params=Params) as Response:
            Data = await Response.json()
    
    return {
        "Status": "Success",
        "SoilProfile": {
            "pH": Data["properties"]["layers"][0]["depths"][0]["values"]["mean"] / 10,
            "ClayContent": Data["properties"]["layers"][1]["depths"][0]["values"]["mean"],
            "SandContent": Data["properties"]["layers"][2]["depths"][0]["values"]["mean"],
            "TotalNitrogen": Data["properties"]["layers"][3]["depths"][0]["values"]["mean"],
            "SoilTexture": ClassifySoilTexture(
                Clay=Data["properties"]["layers"][1]["depths"][0]["values"]["mean"],
                Sand=Data["properties"]["layers"][2]["depths"][0]["values"]["mean"]
            )
        },
        "Source": "ISRIC SoilGrids",
        "Timestamp": datetime.now().isoformat()
    }
```

### **Tool Error Handling**

All Tools Implement Graceful Degradation:

```python
async def WeatherTool(Location: str, DaysAhead: int, ToolContext: ToolContext) -> Dict[str, Any]:
    try:
        # Primary API Call
        Data = await FetchFromOpenWeatherMap(Location)
        return {"Status": "Success", "Data": Data}
    except APITimeout:
        # Retry Once
        Logger.warning("API Timeout, Retrying...")
        Data = await FetchFromOpenWeatherMap(Location)
        return {"Status": "Success", "Data": Data}
    except APIError as E:
        # Fallback To Historical Average
        Logger.error(f"API Failed: {E}, Using Historical Average")
        Data = await GetHistoricalAverage(Location)
        return {"Status": "Partial", "Data": Data, "Source": "Historical"}
    except Exception as E:
        # Final Fallback
        Logger.error(f"Critical Error: {E}")
        return {"Status": "Error", "Message": str(E)}
```

---

## Data Flow

### **End-To-End Request Flow**

```
┌──────────────────────────────────────────────────────────────────────┐
│ 1. User Submits Request Via Web UI                                   │
│    Location: "Punjab, India"                                         │
│    DaysAhead: 30                                                     │
│    Email: "farmer@example.com"                                       │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 2. FastAPI Receives Request                                          │
│    • Validates Input (Pydantic)                                      │
│    • Creates Session ID                                              │
│    • Routes To Orchestrator                                          │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 3. OrchestratorAgent Initializes                                     │
│    • Creates Session (InMemorySessionService)                        │
│    • Initializes Memory Bank                                         │
│    • Starts Observability Tracing                                    │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 4. ForecastAgent Executes (Parallel Tools)                           │
│    ┌──────────────────────────────────────────────────────────────┐  │
│    │ Parallel Execution:                                          │  │
│    │ • WeatherTool → OpenWeatherMap API (120ms)                   │  │
│    │ • SatelliteTool → NASA POWER API (150ms)                     │  │
│    │ • CopernicusTool → ESA CDS API (200ms)                       │  │
│    │ • SoilTestTool → ISRIC SoilGrids (80ms)                      │  │
│    │ Total Time: max(120, 150, 200, 80) = 200ms                   │  │
│    └──────────────────────────────────────────────────────────────┘  │
│    • Combines Results Into Risk Assessment                           │
│    • Calculates Drought, Flood, Heat, Disease, Pest Risks            │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 5. VerifyAgent Validates Results                                     │
│    • Google Search For Recent News                                   │
│    • Cross-Check With Historical Data                                │
│    • Calculate Confidence Score (0.0 - 1.0)                          │
│    • Flag Anomalies Or Low-Confidence Results                        │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 6. Decision Point: Confidence Check                                  │
│    If Confidence < 0.7:                                              │
│    • Loop Back To ForecastAgent With Feedback                        │
│    • Max 3 Iterations                                                │
│    Else:                                                             │
│    • Proceed To PlannerAgent                                         │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 7. PlannerAgent Creates Action Plan                                  │
│    • Generate Prioritized Action Items                               │
│    • Map To Local Resources (E.g., Irrigation Schemes)               │
│    • Create HTML Email Report                                        │
│    • Send Email Via SMTP                                             │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 8. OrchestratorAgent Synthesizes Response                            │
│    • Combine Forecast + Verify + Planner Results                     │
│    • Store In Memory Bank For Future Reference                       │
│    • Update Session State                                            │
│    • Return Unified JSON Response                                    │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 9. FastAPI Returns Response To Web UI                                │
│    • JSON Response With Risk Assessment                              │
│    • Action Plan                                                     │
│    • Email Confirmation                                              │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 10. Web UI Displays Results                                          │
│    • Render Risk Assessment With Color Coding                        │
│    • Show Action Plan                                                │
│    • Display Email Sent Confirmation                                 │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Session & Memory Management

### **Session State Architecture**

```python
# Session State Structure
SessionState = {
    "SessionId": "session-abc-123",
    "CreatedAt": "2024-12-15T10:30:00Z",
    "UserId": "farmer@example.com",
    "FarmerProfile": {
        "Name": "Rajesh Kumar",
        "Location": "Punjab, India",
        "Crops": ["Wheat", "Rice"],
        "FarmSize": "5 Acres"
    },
    "ConversationHistory": [
        {
            "Role": "User",
            "Message": "What Are The Risks For My Farm?",
            "Timestamp": "2024-12-15T10:30:00Z"
        },
        {
            "Role": "Assistant",
            "Message": "Based On Analysis, High Drought Risk Detected...",
            "Timestamp": "2024-12-15T10:30:15Z"
        }
    ],
    "CurrentContext": {
        "LastQuery": "What Are The Risks For My Farm?",
        "LastRiskAssessment": {...},
        "LastActionPlan": [...]
    }
}
```

### **Memory Bank Structure**

```python
# Long-Term Memory Structure
MemoryBank = {
    "FarmerProfile": {
        "Email": "farmer@example.com",
        "Location": "Punjab, India",
        "Crops": ["Wheat", "Rice"],
        "JoinedDate": "2024-01-01"
    },
    "RiskHistory": [
        {
            "Date": "2024-12-01",
            "Risks": {"Drought": "High", "Flood": "Low"},
            "Outcome": "Irrigation Increased, No Crop Loss"
        },
        {
            "Date": "2024-11-15",
            "Risks": {"Heat": "Medium", "Pest": "Low"},
            "Outcome": "Mulching Applied, Minor Leaf Damage"
        }
    ],
    "PreferredActions": [
        "Email Notifications",
        "SMS Disabled",
        "Hindi Language Preferred"
    ],
    "LearningInsights": [
        "Farmer Responds Well To Visual Risk Charts",
        "Prefers Morning Notifications (6-8 AM)",
        "Often Asks About Pest Management"
    ]
}
```

### **Context Compaction Strategy**

```python
def CompactContext(ConversationHistory: List[Dict]) -> List[Dict]:
    """
    Reduce Token Count While Preserving Key Information.
    
    Strategy:
    1. Keep Last 5 Messages In Full
    2. Summarize Older Messages Into Key Facts
    3. Extract Critical Entities (Dates, Locations, Risks)
    """
    
    if len(ConversationHistory) <= 5:
        return ConversationHistory
    
    # Separate Recent And Old Messages
    RecentMessages = ConversationHistory[-5:]
    OldMessages = ConversationHistory[:-5]
    
    # Summarize Old Messages
    Summary = {
        "Role": "System",
        "Message": f"Summary Of {len(OldMessages)} Earlier Messages: " + 
                   f"User Asked About Risks For {ExtractLocation(OldMessages)}. " +
                   f"Key Concerns: {ExtractKeywords(OldMessages)}.",
        "Timestamp": OldMessages[0]["Timestamp"]
    }
    
    return [Summary] + RecentMessages
```

---

## Observability Architecture

### **Logging Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                  LOGGING INFRASTRUCTURE                     │
├─────────────────────────────────────────────────────────────┤
│  Application Code                                           │
│         │                                                   │
│         ▼                                                   │
│  Python Logging Module                                      │
│         │                                                   │
│         ├──▶ Console Handler (Development)                 │
│         │         │                                         │
│         │         ▼                                         │
│         │    STDOUT (JSON Format)                           │
│         │                                                   │
│         └──▶ File Handler (Production)                     │
│                   │                                         │
│                   ▼                                         │
│              app.log (Rotation: 10MB, 5 Files)              │
│                   │                                         │
│                   ▼                                         │
│         Log Aggregation (Future: ELK/Splunk)                │
└─────────────────────────────────────────────────────────────┘
```

### **Tracing Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                 DISTRIBUTED TRACING FLOW                    │
├─────────────────────────────────────────────────────────────┤
│  User Request (Trace ID: xyz-789)                           │
│         │                                                   │
│         ▼                                                   │
│  OrchestratorAgent (Span: orchestrator.execute)             │
│         │                                                   │
│         ├──▶ ForecastAgent (Span: forecast.run)            │
│         │         │                                         │
│         │         ├──▶ WeatherTool (Span: tool.weather)    │
│         │         ├──▶ SatelliteTool (Span: tool.satellite)│
│         │         └──▶ CopernicusTool (Span: tool.copern)  │
│         │                                                   │
│         ├──▶ VerifyAgent (Span: verify.validate)           │
│         │                                                   │
│         └──▶ PlannerAgent (Span: planner.create)           │
│                                                             │
│  All Spans Exported To OpenTelemetry Collector              │
│         │                                                   │
│         ▼                                                   │
│  Jaeger/Zipkin (Trace Visualization)                        │
└─────────────────────────────────────────────────────────────┘
```

### **Metrics Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    METRICS COLLECTION                       │
├─────────────────────────────────────────────────────────────┤
│  Application Code (@record_agent_duration)                  │
│         │                                                   │
│         ▼                                                   │
│  Prometheus Client Library                                  │
│         │                                                   │
│         ├──▶ In-Memory Metrics Registry                    │
│         │         │                                         │
│         │         ├─ agent_execution_seconds (Histogram)    │
│         │         ├─ tool_calls_total (Counter)             │
│         │         ├─ agent_errors_total (Counter)           │
│         │         └─ agent_iterations_total (Counter)       │
│         │                                                   │
│         ▼                                                   │
│  /metrics HTTP Endpoint (Prometheus Format)                 │
│         │                                                   │
│         ▼                                                   │
│  Prometheus Server (Scrapes Every 15s)                      │
│         │                                                   │
│         ▼                                                   │
│  Grafana (Visualization & Alerting)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

### **Local Development**

```
┌────────────────────────────────────────────────────────┐
│            LOCALHOST (127.0.0.1)                       │
├────────────────────────────────────────────────────────┤
│  FastAPI Main App      (Port 8000)                     │
│  OrchestratorServer    (Port 9000)                     │
│  ForecastServer        (Port 9001)                     │
│  VerifyServer          (Port 9002)                     │
│  PlannerServer         (Port 9003) [Future]            │
└────────────────────────────────────────────────────────┘
```

### **Production Deployment (Docker)**

```
┌────────────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE STACK                        │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ agrisense-web        │  │ agrisense-orchestr   │            │
│  │ (FastAPI + UI)       │  │ (OrchestratorAgent)  │            │
│  │ Port: 8000           │  │ Port: 9000           │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ agrisense-forecast   │  │ agrisense-verify     │            │
│  │ (ForecastAgent)      │  │ (VerifyAgent)        │            │
│  │ Port: 9001           │  │ Port: 9002           │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ prometheus           │  │ grafana              │            │
│  │ (Metrics)            │  │ (Visualization)      │            │
│  │ Port: 9090           │  │ Port: 3000           │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                │
│  Network: agrisense-network (Bridge)                           │
└────────────────────────────────────────────────────────────────┘
```

### **Cloud Deployment (Google Cloud Run)**

```
┌───────────────────────────────────────────────────────────────┐
│                    GOOGLE CLOUD ARCHITECTURE                  │
├───────────────────────────────────────────────────────────────┤
│  Cloud Load Balancer                                          │
│         │                                                     │
│         ├──▶ agrisense-web (Cloud Run)                       │
│         │         │                                           │
│         │         ├──▶ agrisense-orchestrator (Cloud Run)    │
│         │         │         │                                 │
│         │         │         ├──▶ agrisense-forecast (Run)    │
│         │         │         ├──▶ agrisense-verify (Run)      │
│         │         │         └──▶ agrisense-planner (Run)     │
│         │         │                                           │
│         │         └──▶ Cloud Firestore (Session Storage)     │
│         │                                                     │
│         └──▶ Cloud Monitoring (Logs, Traces, Metrics)        │
│                                                               │
│  External APIs:                                               │
│  • OpenWeatherMap                                             │
│  • NASA POWER                                                 │
│  • Copernicus CDS                                             │
│  • ISRIC SoilGrids                                            │
└───────────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### **API Key Management**

```
┌─────────────────────────────────────────────────────────┐
│              SECRETS MANAGEMENT STRATEGY                │
├─────────────────────────────────────────────────────────┤
│  Development:                                           │
│  • .env File (Gitignored)                               │
│  • Environment Variables                                │
│                                                         │
│  Production:                                            │
│  • Google Secret Manager                                │
│  • Environment Variables Injected At Runtime            │
│  • Kubernetes Secrets (If Using K8s)                    │
└─────────────────────────────────────────────────────────┘
```

### **Input Validation**

```python
class ForecastRequest(BaseModel):
    """Pydantic Model For Input Validation"""
    Location: str = Field(..., min_length=1, max_length=200)
    FarmerEmail: EmailStr = Field(...)
    DaysAhead: int = Field(default=30, ge=1, le=90)
    
    @field_validator('Location')
    @classmethod
    def validate_location(cls, v):
        # Prevent SQL Injection, XSS
        if re.search(r'[<>"\';]', v):
            raise ValueError("Invalid Characters In Location")
        return v.strip()
```

### **Rate Limiting**

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

Limiter = Limiter(key_func=get_remote_address)

@app.post("/forecast")
@Limiter.limit("10/minute")
async def Forecast(request: ForecastRequest):
    # API Handler
    pass
```

---

## Performance Optimization

### **Caching Strategy**

```python
from functools import lru_cache
import redis

# In-Memory Cache For Static Data
@lru_cache(maxsize=1000)
async def GeocodeLocation(Location: str) -> Tuple[float, float]:
    """Cache Geocoding Results To Avoid Repeated API Calls"""
    pass

# Redis Cache For Dynamic Data (Future)
RedisClient = redis.Redis(host='localhost', port=6379, db=0)

async def GetWeatherData(Location: str):
    # Check Cache First
    CacheKey = f"weather:{Location}"
    Cached = RedisClient.get(CacheKey)
    if Cached:
        return json.loads(Cached)
    
    # Fetch From API
    Data = await FetchFromAPI(Location)
    
    # Cache For 1 Hour
    RedisClient.setex(CacheKey, 3600, json.dumps(Data))
    
    return Data
```

### **Database Connection Pooling**

```python
# For Future Database Integration
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/agrisense",
    pool_size=20,
    max_overflow=10
)

AsyncSessionLocal = sessionmaker(
    Engine, class_=AsyncSession, expire_on_commit=False
)
```

---

## Scalability Considerations

### **Horizontal Scaling**

```
┌────────────────────────────────────────────────────────┐
│              LOAD BALANCER (Nginx/GCP LB)              │
└───────────────────────┬────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Web Instance │ │ Web Instance │ │ Web Instance │
│      #1      │ │      #2      │ │      #3      │
└──────────────┘ └──────────────┘ └──────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Orchestrator │ │ Orchestrator │ │ Orchestrator │
│ Instance #1  │ │ Instance #2  │ │ Instance #3  │
└──────────────┘ └──────────────┘ └──────────────┘
```

### **Message Queue (Future)**

```
┌────────────────────────────────────────────────────────┐
│              ASYNC TASK PROCESSING                     │
├────────────────────────────────────────────────────────┤
│  Web API                                               │
│     │                                                  │
│     ├──▶ Publish Task To Queue (RabbitMQ/Cloud Tasks) │
│     │                                                  │
│     └──▶ Return Task ID Immediately To User           │
│                                                        │
│  Background Workers (Celery/Cloud Functions)           │
│     │                                                  │
│     ├──▶ Consume Task From Queue                      │
│     │                                                  │
│     ├──▶ Execute Long-Running Forecast                │
│     │                                                  │
│     └──▶ Update Task Status In Database               │
│                                                        │
│  Polling Endpoint                                      │
│     │                                                  │
│     └──▶ User Polls /task/{id}/status For Results     │
└────────────────────────────────────────────────────────┘
```

---

## Conclusion

AgriSenseGuardian's Architecture Demonstrates:

✅ **Modern Multi-Agent Design** — Google ADK + A2A Protocol  
✅ **Scalable Infrastructure** — Async, Microservices-Ready  
✅ **Production-Grade Observability** — Logging, Tracing, Metrics  
✅ **Robust Error Handling** — Graceful Degradation At Every Layer  
✅ **Farmer-Centric Design** — Simple UI, Complex Backend  

**Built For Scale. Designed For Impact. Powered By AI.**

---

<div align="center">

**📚 Related Documentation**

[README.md](../README.md) | [CHANGELOG.md](../CHANGELOG.md) | [SETUP_GUIDE.md](../Setup/SETUP_GUIDE.md)

---

**🌾 AgriSenseGuardian — Architected With Excellence**

</div>
