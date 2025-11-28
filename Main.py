"""
╔══════════════════════════════════════════════════════════════════════════╗
║  AgriSenseGuardian — Main Application Entry Point                        ║
║  Launches Web UI + A2A Multi-Agent System                                ║
║  Built For: Kaggle X Google Capstone Hackathon                           ║
║  Author: Anubhav Chaurasia (i8o8i)                                       ║
╚══════════════════════════════════════════════════════════════════════════╝

This Module Serves As The Central Hub For AgriSenseGuardian, An AI-Powered
Agricultural Decision Support System. It Orchestrates A Multi-Agent Architecture
Using Google's ADK And A2A Protocols To Provide Real-Time Risk Assessments
And Actionable Recommendations For Indian Farmers.

Key Responsibilities:
- Initialize And Manage The FastAPI Web Application
- Bootstrap A2A Agent Servers For Distributed Processing
- Handle HTTP Requests For Forecasts, Health Checks, And Task Management
- Provide Web UI For User Interaction
- Ensure Proper Startup/Shutdown Lifecycles With Observability

The System Integrates Real-World Data From Weather APIs, Satellite Imagery,
And Climate Models To Deliver Accurate, Localized Agricultural Insights.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from contextlib import asynccontextmanager

# Ensure Parent Directory Is In sys.path For Seamless Absolute Imports Across Modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# FastAPI Ecosystem Imports For Building Robust Web APIs
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr, field_validator

# Internal Module Imports For Core Functionality
from Config.Settings import get_settings
from Services.AgentBootstrap import AgentBootstrap
from Services.HealthService import HealthService
from Agents.OrchestratorAgent import OrchestratorAgent
from Utils.Logger import SetupLogger as GetLogger
from Services.TaskManager import get_task_manager
from Utils.Observability import setup_tracing, metrics_response, use_span, record_agent_duration

# ===== CONFIGURATION =====
Settings = get_settings()
Logger = GetLogger(__name__)

# ===== GLOBAL STATE =====
AgentBootstrapInstance = None
OrchestratorInstance = None
HealthServiceInstance = None

# ===== REQUEST/RESPONSE MODELS =====


class ForecastRequest(BaseModel):
    """Request Model For Initiating An Agricultural Forecast Workflow.

    This Model Captures All Necessary Information To Generate Comprehensive
    Risk Assessments And Action Plans For A Specific Farm Location.
    """
    Location: str = Field(..., min_length=1, description="Farm Location (City, Village, Or Coordinates)")
    FarmerPhone: str | None = Field(None, min_length=10, description="Farmer's Mobile Number (Optional - Email Is Primary)")
    FarmerEmail: EmailStr = Field(..., description="Farmer's Email Address (Required For Notifications)")
    DaysAhead: int = Field(default=30, ge=1, le=90, description="Forecast Horizon In Days")
    UserQuery: str = Field(default="What Are The Agricultural Risks For My Farm?", description="Custom User Query")

    @field_validator('FarmerEmail')
    @classmethod
    def validate_email_not_empty(cls, v):
        """Ensure Email Is Not Empty Or Whitespace-Only."""
        if not v or not v.strip():
            raise ValueError('FarmerEmail Must Be Provided And Cannot Be Empty')
        return v.strip()


class HealthResponse(BaseModel):
    """
    Response Model For Health Check Endpoints.
    
    Provides System Status Information Including Web UI Access
    And Agent Availability For Monitoring And Debugging Purposes.
    """
    Status: str
    Message: str
    WebUI: str
    AgentsRunning: bool


    """
    Request Model For Initiating Long-Running Forecast Tasks.

    Allows Configuration Of Confidence Thresholds And Iteration Limits
    For Advanced Users Who Need Fine-Tuned Control Over The Analysis Process.
    """
class LongForecastRequest(BaseModel):
    Location: str = Field(..., min_length=1)
    FarmerPhone: str | None = Field(None, min_length=10)
    FarmerEmail: EmailStr = Field(..., description="Farmer's Email Address (Required For Notifications)")
    DaysAhead: int = Field(default=30, ge=1, le=90)
    UserQuery: str = Field(default="What Are The Agricultural Risks For My Farm?")

    @field_validator('FarmerEmail')
    @classmethod
    def validate_email_not_empty(cls, v):
        """Ensure Email Is Not Empty Or Whitespace-Only."""
        if not v or not v.strip():
            raise ValueError('FarmerEmail must be provided and cannot be empty')
        return v.strip()
    ConfidenceThreshold: int = Field(default=75, ge=0, le=100)
    MaxIterations: int = Field(default=2, ge=1, le=5)


# Alias For Task Start Requests — Uses Same Fields As LongForecastRequest
class TaskStartRequest(LongForecastRequest):
    """Request Model For Starting A Long-Running Forecast As A Background Task.

    This Is Intentionally A Subclass Of `LongForecastRequest` To Avoid
    Duplication While Providing A Clear Name For Task-Related Endpoints.
    """
    pass


# ===== LIFESPAN MANAGEMENT =====
@asynccontextmanager
async def Lifespan(App: FastAPI):
    """
    Manages The Complete Application Lifecycle From Startup To Shutdown.
    
    This Async Context Manager Ensures Proper Initialization Of All Components:
    - Launches A2A Agent Servers For Distributed Processing If Enabled
    - Initializes The Orchestrator For In-Process Workflows  
    - Sets Up Health Monitoring And Observability
    - Handles Graceful Cleanup During Shutdown
    
    The Lifespan Approach Guarantees That Resources Are Properly Managed
    And That The Application State Remains Consistent Throughout Its Runtime.
    """
    global AgentBootstrapInstance, OrchestratorInstance, HealthServiceInstance
    
    Logger.info("🚀 Starting AgriSenseGuardian Application...")
    
    # Initialize Health Service For System Monitoring
    HealthServiceInstance = HealthService()
    # Setup Tracing/Telemetry If Available (No-Op If Not Installed)
    try:
        setup_tracing("AgriSenseGuardian")
    except Exception:
        pass
    
    Logger.info("🚀 Starting AgriSenseGuardian Application...")
    
    # Initialize Health Service
    HealthServiceInstance = HealthService()
    # Setup Tracing/Telemetry If Available (No-Op If Not Installed)
    try:
        setup_tracing("AgriSenseGuardian")
    except Exception:
        pass
    
    # Start A2A Agents If Enabled
    if Settings.start_a2a_on_startup:
        Logger.info("🤖 A2A Auto-Start Enabled - Launching Multi-Agent System...")
        try:
            AgentBootstrapInstance = AgentBootstrap()
            AgentBootstrapInstance.start_all()
            
            # Allow Time For Agents To Fully Initialize Before Health Checks
            await asyncio.sleep(5)
            
            # Perform Comprehensive Health Validation Of All A2A Agents
            AgentHealthDict = HealthServiceInstance.check_a2a_agents()
            AllHealthy = all(agent.port_open for agent in AgentHealthDict.values())
            if AllHealthy:
                Logger.info(f"✅ All A2A Agents Running: {list(AgentHealthDict.keys())}")
            else:
                Failed = [name for name, agent in AgentHealthDict.items() if not agent.port_open]
                Logger.warning(f"⚠️ Some Agents Not Ready: {Failed}")
                
        except Exception as E:
            Logger.error(f"❌ Failed To Start A2A Agents: {E}")
            Logger.warning("⚠️ Continuing With In-Process Mode Only")
    else:
        Logger.info("ℹ️ A2A Auto-Start Disabled (Set START_A2A_ON_STARTUP=true To Enable)")
    
    # Initialize Core Orchestrator Agent For Workflow Coordination
    Logger.info("🧠 Initializing Orchestrator Agent...")
    OrchestratorInstance = OrchestratorAgent()
    
    Logger.info("✅ AgriSenseGuardian Ready!")
    Logger.info(f"🌐 Web UI: http://{Settings.api_host}:{Settings.api_port}")
    Logger.info(f"📡 API Endpoint: http://{Settings.api_host}:{Settings.api_port}/forecast")
    
    if Settings.start_a2a_on_startup:
        Logger.info(f"🤖 A2A Orchestrator: http://{Settings.a2a_host}:{Settings.a2a_ports.orchestrator_port}")
        Logger.info(f"🔬 A2A Forecast: http://{Settings.a2a_host}:{Settings.a2a_ports.forecast_port}")
        Logger.info(f"✅ A2A Verify: http://{Settings.a2a_host}:{Settings.a2a_ports.verify_port}")
    
    yield  # Application Running
    
    # Perform Graceful Shutdown Sequence
    Logger.info("🛑 Shutting Down AgriSenseGuardian...")
    
    if AgentBootstrapInstance:
        Logger.info("🔄 Stopping A2A Agents...")
        AgentBootstrapInstance.stop_all()
    
    Logger.info("👋 AgriSenseGuardian Stopped Successfully")


# ===== FASTAPI APPLICATION =====
App = FastAPI(
    title="AgriSenseGuardian",
    description="AI-Powered Agricultural Decision Support System Using Multi-Agent Architecture",
    version="1.0.0",
    lifespan=Lifespan
)

# Enable Cross-Origin Resource Sharing For Web UI Integration
App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Static File Serving And Template Engine
CurrentDir = Path(os.path.abspath(os.path.dirname(__file__)))
StaticDir = CurrentDir / "Static"
TemplatesDir = CurrentDir / "Templates"

App.mount("/Static", StaticFiles(directory=str(StaticDir)), name="static")
Templates = Jinja2Templates(directory=str(TemplatesDir))


# ===== ROUTES =====

@App.get("/", response_class=HTMLResponse)
async def Index(Request: Request):
    """
    Serve The Main Web User Interface.
    
    This Endpoint Renders The Primary Dashboard Where Farmers Can:
    - Input Their Location And Contact Information
    - Submit Custom Queries About Their Crops
    - View Real-Time Risk Assessments And Recommendations
    - Access Historical Analysis And Trends
    """
    return Templates.TemplateResponse("index.html", {"request": Request})

@App.get("/health")
async def Health():
    """
    Provide Basic System Health Status.
    
    Returns A Simple Health Check Response Indicating Whether The Core
    Application Is Running And Accessible. Used By Load Balancers And
    Monitoring Systems For Basic Availability Checks.
    """
    return HealthResponse(
        Status="healthy",
        Message="AgriSenseGuardian Is Running",
        WebUI=f"http://{Settings.api_host}:{Settings.api_port}",
        AgentsRunning=AgentBootstrapInstance is not None and AgentBootstrapInstance.status()['running_count'] > 0
    )


@App.get("/readiness")
async def Readiness():
    """
    Perform Comprehensive Readiness Assessment Of All System Components.
    
    This Detailed Health Check Evaluates:
    - Web UI Availability
    - Orchestrator Agent Initialization
    - A2A Agent Server Status And Port Accessibility
    - Bootstrap Service Health And Agent Counts
    
    Used For Kubernetes Readiness Probes And Advanced Monitoring.
    """

    ReadinessData = {
        "WebUI": "Ready",
        "OrchestratorAgent": "Ready" if OrchestratorInstance else "NotInitialized"
    }
    
    # Check A2A Agent Health If Running
    if HealthServiceInstance and Settings.start_a2a_on_startup:
        AgentHealthDict = HealthServiceInstance.check_a2a_agents()
        ReadinessData["A2AAgents"] = {
            "AllHealthy": all(agent.port_open for agent in AgentHealthDict.values()),
            "Agents": {name: {"port_open": agent.port_open, "http_status": agent.http_status} 
                      for name, agent in AgentHealthDict.items()}
        }
    else:
        ReadinessData["A2AAgents"] = "NotEnabled"
    
    # Check Bootstrap Status
    if AgentBootstrapInstance:
        BootstrapStatus = AgentBootstrapInstance.status()
        ReadinessData["Bootstrap"] = {
            "RunningCount": BootstrapStatus['running_count'],
            "TotalCount": BootstrapStatus['total_count'],
            "Agents": BootstrapStatus['agents']
        }
    else:
        ReadinessData["Bootstrap"] = "NotStarted"
    
    return JSONResponse(content=ReadinessData)


@App.post("/forecast")
async def Forecast(ForecastReq: ForecastRequest):
    """
    Execute The Complete Multi-Agent Agricultural Forecast Workflow.
    
    This Is The Primary API Endpoint That Orchestrates The Entire Analysis Process:
    1. Validates The Incoming Request Parameters
    2. Triggers The Orchestrator Agent To Coordinate Forecast → Verify → Planner Sequence
    3. Returns A Comprehensive Response With Risk Assessments, Verification Scores, And Action Plans
    
    The Workflow Integrates Real-Time Data From Weather APIs, Satellite Imagery,
    And Climate Models To Provide Actionable Agricultural Intelligence.
    """
    Logger.info(f"📥 Forecast Request Received: Location={ForecastReq.Location}, Days={ForecastReq.DaysAhead}")
    
    try:
        # Validate That Orchestrator Is Properly Initialized
        if not OrchestratorInstance:
            raise HTTPException(status_code=503, detail="Orchestrator Agent Not Initialized")
        
        Logger.info("🧠 Executing Orchestrator Workflow...")
        
        with record_agent_duration("OrchestratorWorkflow"), use_span("HTTP.Forecast"):
            try:
                Result = await OrchestratorInstance.ExecuteWorkflow(
                    Location=ForecastReq.Location,
                    DaysAhead=ForecastReq.DaysAhead,
                    FarmerPhone=ForecastReq.FarmerPhone,
                    FarmerEmail=ForecastReq.FarmerEmail,
                    UserQuery=ForecastReq.UserQuery
                )
            except Exception as WorkflowError:
                Logger.error(f"❌ Workflow Execution Error: {WorkflowError}", exc_info=True)
                raise
        
        # Check If Workflow Returned Error
        if Result.get('Status') == 'Error':
            Logger.error(f"❌ Workflow Failed: {Result.get('Message', 'Unknown error')}")
            Logger.error(f"📋 Execution History: {Result.get('ExecutionHistory', [])}")
        else:
            Logger.info(f"✅ Forecast Completed Successfully For {ForecastReq.Location}")
            Logger.info(f"⏱️ Execution Time: {Result.get('ExecutionSummary', {}).get('TotalDuration', 'N/A')}")
        
        # Log Response Structure For Debugging
        Logger.info(f"📦 Response Keys: {list(Result.keys())}")
        if 'ForecastResults' in Result:
            Logger.info(f"📊 ForecastResults Keys: {list(Result['ForecastResults'].keys()) if isinstance(Result['ForecastResults'], dict) else type(Result['ForecastResults'])}")
        if 'ActionPlan' in Result:
            Logger.info(f"📋 ActionPlan Keys: {list(Result['ActionPlan'].keys()) if isinstance(Result['ActionPlan'], dict) else type(Result['ActionPlan'])}")
        
        return JSONResponse(content=Result)
        
    except Exception as E:
        Logger.error(f"❌ Forecast Failed: {str(E)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Forecast Generation Failed: {str(E)}"
        )


@App.get("/agents/status")
async def AgentsStatus():
    """
    Retrieve Comprehensive Status Information For All A2A Agent Instances.
    
    This Administrative Endpoint Provides Detailed Insights Into The Multi-Agent
    System, Including Process Status, Port Availability, And Health Metrics.
    Essential For Monitoring Distributed Agent Performance And Troubleshooting.
    """
    if not AgentBootstrapInstance:
        return JSONResponse(content={
            "Status": "NotRunning",
            "Message": "A2A Agents Not Started (Set START_A2A_ON_STARTUP=true)",
            "Agents": []
        })
    
    BootstrapStatus = AgentBootstrapInstance.status()
    
    # Augment With Detailed Health Diagnostics From Health Service
    if HealthServiceInstance:
        AgentHealthDict = HealthServiceInstance.check_a2a_agents()
        BootstrapStatus["HealthCheck"] = {
            "AllHealthy": all(agent.port_open for agent in AgentHealthDict.values()),
            "Agents": {name: {"port_open": agent.port_open, "http_status": agent.http_status} 
                      for name, agent in AgentHealthDict.items()}
        }
    
    return JSONResponse(content=BootstrapStatus)


@App.post("/agents/restart")
async def RestartAgents():
    """
    Perform A Complete Restart Of All A2A Agent Processes.
    
    This Administrative Endpoint Gracefully Shuts Down All Running Agents,
    Waits For Cleanup, Then Reinitializes The Entire Multi-Agent System.
    Useful For Applying Configuration Changes Or Recovering From Agent Failures.
    """
    if not AgentBootstrapInstance:
        raise HTTPException(status_code=400, detail="A2A Agents Not Initialized")
    
    try:
        Logger.info("🔄 Restarting All A2A Agents...")
        AgentBootstrapInstance.stop_all()
        await asyncio.sleep(2)  # Allow Time For Clean Shutdown
        AgentBootstrapInstance.start_all()
        await asyncio.sleep(5)  # Allow Time For Initialization
        
        Logger.info("✅ A2A Agents Restarted")
        return {"Status": "Success", "Message": "All Agents Restarted"}
        
    except Exception as E:
        Logger.error(f"❌ Restart Failed: {E}")
        raise HTTPException(status_code=500, detail=f"Restart Failed: {str(E)}")


@App.get("/metrics")
async def Metrics():
    """
    Expose Prometheus-Style Metrics For System Monitoring.
    
    Returns Real-Time Telemetry Data Including Agent Execution Times,
    Tool Invocation Counts, And System Health Indicators. Used By
    Monitoring Dashboards And Alerting Systems For Operational Insights.
    """
    body, ctype = metrics_response()
    return Response(content=body, media_type=ctype)


# ===== Long-Running Task Endpoints =====

@App.post("/tasks/start")
async def StartTask(req: TaskStartRequest):
    if not OrchestratorInstance:
        raise HTTPException(status_code=503, detail="Orchestrator Agent Not Initialized")

    Mgr = get_task_manager()

    async def runner(task_id: str):
        with record_agent_duration("OrchestratorWorkflow"), use_span("Task.Forecast"):
            return await OrchestratorInstance.ExecuteWorkflow(
                Location=req.Location,
                DaysAhead=req.DaysAhead,
                FarmerPhone=req.FarmerPhone,
                FarmerEmail=req.FarmerEmail,
                UserQuery=req.UserQuery,
                ConfidenceThreshold=req.ConfidenceThreshold,
                MaxIterations=req.MaxIterations,
                TaskId=task_id
            )

    task_id = await Mgr.start(runner)
    return {"Status": "Accepted", "TaskId": task_id, "Message": "Task Started"}


@App.post("/tasks/{task_id}/pause")
async def PauseTask(task_id: str):
    """Pause A Long-Running Forecast Task For Later Resumption."""
    Mgr = get_task_manager()
    return await Mgr.pause(task_id)


@App.post("/tasks/{task_id}/resume")
async def ResumeTask(task_id: str):
    """Resume A Previously Paused Forecast Task."""
    Mgr = get_task_manager()
    return await Mgr.resume(task_id)


@App.post("/tasks/{task_id}/cancel")
async def CancelTask(task_id: str):
    """Cancel A Running Or Paused Forecast Task."""
    Mgr = get_task_manager()
    return await Mgr.cancel(task_id)


@App.get("/tasks/{task_id}/status")
async def TaskStatus(task_id: str):
    """Retrieve Current Status And Progress Of A Specific Task."""
    Mgr = get_task_manager()
    return Mgr.status(task_id)


# ===== EXCEPTION HANDLERS =====

@App.exception_handler(404)
async def NotFoundHandler(Request: Request, Exc):
    """
    Handle Requests To Non-Existent Endpoints.
    
    Provides A Consistent Error Response For Invalid API Paths,
    Helping Developers Debug Integration Issues.
    """
    return JSONResponse(
        status_code=404,
        content={
            "Status": "error",
            "Message": "Endpoint Not Found",
            "Path": str(Request.url)
        }
    )


@App.exception_handler(500)
async def InternalErrorHandler(Request: Request, Exc):
    """
    Handle Unexpected Server Errors.
    
    Logs Detailed Error Information For Debugging While Returning
    A User-Friendly Error Response To Prevent Information Disclosure.
    """
    Logger.error(f"Internal Server Error: {Exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "Status": "error",
            "Message": "Internal Server Error",
            "Detail": str(Exc)
        }
    )


# ===== MAIN ENTRY POINT =====

def Main():
    """
    Application Entry Point For AgriSenseGuardian.
    
    Initializes Logging, Displays System Information, And Starts The FastAPI
    Server Using Uvicorn. This Function Is Called When The Module Is Executed
    Directly And Serves As The Primary Launch Mechanism For The Application.
    """
    import uvicorn
    
    Logger.info("=" * 80)
    Logger.info("🌾 AgriSenseGuardian — Agricultural AI Decision Support System")
    Logger.info("=" * 80)
    Logger.info(f"📍 Working Directory: {os.getcwd()}")
    Logger.info(f"🐍 Python Version: {sys.version.split()[0]}")
    Logger.info(f"🌐 Server Endpoint: {Settings.api_host}:{Settings.api_port}")
    Logger.info(f"🤖 A2A Multi-Agent Mode: {'Enabled' if Settings.start_a2a_on_startup else 'Disabled'}")
    Logger.info("=" * 80)
    
    try:
        # Start The ASGI Server With Production-Ready Configuration
        uvicorn.run(
            "Main:App",
            host=Settings.api_host,
            port=Settings.api_port,
            reload=False,  # Set True For Development
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        Logger.info("\n🛑 Received Shutdown Signal")
    except Exception as E:
        Logger.error(f"❌ Fatal Error: {E}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    Main()