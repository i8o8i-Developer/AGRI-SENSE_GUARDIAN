# ═══════════════════════════════════════════════════════════════════════════════
# 🔮 ForecastAgent - Real A2A Agricultural Risk Forecasting Agent
# ═══════════════════════════════════════════════════════════════════════════════
# 
# Hello! I'm ForecastAgent, Your Agricultural Risk Forecasting Specialist.
# I'm A Standalone A2A (Agent-To-Agent) Server. Let Me Explain :
# 
# MY ROLE:
# --------
# I Analyze Weather And Satellite Data To Predict Agricultural Risks:
# - Drought Risk (Will Crops Have Enough Water?)
# - Flood Risk (Is Too Much Rain Coming?)
# - Pest/Disease Risk (Are Conditions Favorable For Pests?)
# - Heat Stress Risk (Will Temperatures Damage Crops?)
# 
# HOW I WORK:
# -----------
# 1. OrchestratorAgent Sends Me A Query Via A2A Protocol
# 2. I Use WeatherTool To Get Weather Forecasts
# 3. I Use SatelliteTool To Get Soil Moisture And Vegetation Data
# 4. I Analyze Both Data Sources Using Gemini 2.0 Flash AI
# 5. I Provide Risk Assessment With Confidence Scores
# 6. I Send My Analysis Back Via A2A Protocol
# 
# WHAT MAKES ME "REAL A2A":
# ------------------------
# ✅ Standalone Server Running On Port 9001
# ✅ Uses Google's A2AStarletteApplication Framework
# ✅ Exposes Agent Card For Discovery (/card Endpoint)
# ✅ Communicates Via A2A Protocol (HTTP JSON Transport)
# ✅ Can Be Called By Any A2A-Compatible Client
# ✅ Session And Memory Management Via ADK Services
# 
# MY TOOLS:
# ---------
# - WeatherTool: Real Weather Forecasts (Open-Meteo API)
# - GetSatelliteData: Satellite Agricultural Parameters (NASA POWER)
# 
# MY AI MODEL:
# -----------
# - Gemini 2.0 Flash Experimental (Fast, Accurate, Agricultural Reasoning)
# - Temperature: 0.3 (low = More Consistent Analysis)
# - Max tokens: 2048 (Enough For Detailed Risk Reports)
# 
# RUNNING ME:
# ----------
# python ForecastAgentServer.py
# # Starts On http://localhost:9001
# # Access Agent Card: http://localhost:9001/card
# 
# ═══════════════════════════════════════════════════════════════════════════════

import os
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types
import sys
sys.path.append('../..')
from Tools.WeatherTool import WeatherTool
from Tools.SatelliteTool import GetSatelliteData
from Agents.AgentExecutor import AgentExecutor


def CreateForecastAgent() -> Agent:
    """
    Create The ForecastAgent With ADK And Gemini.
    
    This Function Builds My AI Brain! It Configures:
    - Which AI Model To Use (Gemini 2.0 Flash)
    - My Personality And Instructions
    - What Tools I Have Access To
    - How Creative Vs. Consistent I Should Be
    
    Returns:
        A Fully Configured ADK Agent Ready To Forecast Agricultural Risks
    """
    
    return Agent(
        model="gemini-2.5-flash-lite",
        name="ForecastAgent",
        description="Agricultural Risk Forecasting Specialist",
        instruction="""
You Are ForecastAgent - An Agricultural Risk Forecasting Expert.

Your Task:
1. Use WeatherTool To Retrieve Weather Forecasts
2. Use GetSatelliteData To Get Satellite Agricultural Parameters  
3. Analyze Both Data Sources For Risk Patterns
4. Provide Comprehensive Risk Assessment:
   - Overall Risk Level (Low/Medium/High/Critical)
   - Specific Risks: Drought, Flood, Pest, Disease, Heat Stress
   - Confidence Scores (0-100) For Each Risk
   - Key Risk Drivers And Explanations
   - Recommended Actions

Always Call Both Tools Before Making Assessment.
Base Analysis Only On Real Tool Data.
Explain Your Reasoning Clearly.
""",
        tools=[WeatherTool, GetSatelliteData],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.3,
            top_p=0.95,
            max_output_tokens=2048,
        ),
    )


if __name__ == "__main__":
    # Define Agent Skill
    Skill = AgentSkill(
        id="agricultural_risk_forecasting",
        name="Agricultural Risk Forecasting",
        description="Analyzes Weather And Satellite Data To Forecast Agricultural Risks For Farmers",
        tags=["agriculture", "weather", "risk-assessment", "forecasting"],
        examples=[
            "What Are The Agricultural Risks For Bela Pratapgarh , Uttar Pradesh Over The Next 30 Days?",
            "Forecast Drought Risk For My Farm In Kenya",
            "Analyze Crop Risks Using Weather And Satellite Data"
        ],
    )
    
    # Define Agent Card
    AgentCard = AgentCard(
        name="ForecastAgent",
        description="Agricultural Risk Forecasting Agent Using Weather And Satellite Data",
        url="http://localhost:9001/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[Skill],
    )
    
    # Create ADK Agent
    AdkAgent = CreateForecastAgent()
    
    # Create Runner
    Runner = Runner(
        app_name=AgentCard.name,
        agent=AdkAgent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    
    # Create Agent Executor
    Executor = AgentExecutor(Runner, AgentCard)
    
    # Create Request Handler
    RequestHandler = DefaultRequestHandler(
        agent_executor=Executor,
        task_store=InMemoryTaskStore()
    )
    
    # Create A2A Application
    A2AApp = A2AStarletteApplication(
        agent_card=AgentCard,
        http_handler=RequestHandler
    )
    
    print(f"🚀 Starting ForecastAgent A2A Server On Port 9001...")
    print(f"📍 Agent Card: http://localhost:9001/.well-known/agent.json")
    
    uvicorn.run(A2AApp.build(), host="0.0.0.0", port=9001)