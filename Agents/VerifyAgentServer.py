# Real A2A Verify Agent Server
# Standalone A2A Agent For Risk Verification

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


def CreateVerifyAgent() -> Agent:
    """Create Real ADK Agent For Verification."""
    
    return Agent(
        model="gemini-2.5-flash-lite",
        name="VerifyAgent",
        description="Risk Verification Specialist",
        instruction="""
You Are VerifyAgent - A Risk Verification Expert.

Your Task:
1. Receive Risk Assessment From ForecastAgent
2. Use WeatherTool And GetSatelliteData To Cross-Check Claims
3. Validate Or Adjust Risk Levels Based On Your Independent Analysis
4. Provide Verification Report:
   - Confirmed Risks (Agree With Forecast)
   - Adjusted Risk Levels (If Discrepancies Found)
   - Conflicting Signals Between Data Sources
   - Confidence Adjustments
   - Additional Warnings Not In Original Forecast

Always Call Tools To Independently Verify.
Highlight Any Discrepancies Between Your Analysis And The Forecast.
Be Objective And Data-Driven.
""",
        tools=[WeatherTool, GetSatelliteData],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,
            top_p=0.9,
            max_output_tokens=2048,
        ),
    )


if __name__ == "__main__":
    # Define Agent Skill
    Skill = AgentSkill(
        id="risk_verification",
        name="Risk Verification",
        description="Verifies And Validates Agricultural Risk Assessments Through Independent Data Analysis",
        tags=["verification", "validation", "quality-assurance", "agriculture"],
        examples=[
            "Verify this Risk Forecast For Accuracy",
            "Cross-check Agricultural Risk Predictions",
            "Validate Drought Risk Assessment"
        ],
    )
    
    # Define Agent Card
    AgentCard = AgentCard(
        name="VerifyAgent",
        description="Risk Verification Agent That Validates Forecasts Using Independent Data Analysis",
        url="http://localhost:9002/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[Skill],
    )
    
    # Create ADK Agent
    AdkAgent = CreateVerifyAgent()
    
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
    
    print(f"🚀 Starting VerifyAgent A2A Server On Port 9002...")
    print(f"📍 Agent Card: http://localhost:9002/.well-known/agent.json")
    
    uvicorn.run(A2AApp.build(), host="0.0.0.0", port=9002)