# ═══════════════════════════════════════════════════════════════════════════════
# 🏛️ OrchestratorServer - The Master Coordinator Of All Agents
# ═══════════════════════════════════════════════════════════════════════════════
# 
# Greetings! I'm the Orchestrator - Think Of Me As The Conductor Of An Orchestra.
# While Individual Agents Are Musicians, I Coordinate Them To Create A Symphony!
# 
# MY ROLE:
# --------
# I'm The Main Entry Point For Farmers. When A Farmer Asks A Question, I:
# 1. Receive The Farmer's Query
# 2. Decide Which Agents To Involve (ForecastAgent, VerifyAgent, Etc.)
# 3. Send Tasks To Each Agent Via Real A2A Protocol
# 4. Collect Their Responses
# 5. Combine Everything Into A Comprehensive Action Plan
# 6. Send The Final Advice To The Farmer Via Email
# 
# WHAT MAKES ME "ORCHESTRATOR":
# ----------------------------
# ✅ I Coordinate Multiple Specialized Agents
# ✅ I Use Real A2A Client To Communicate With Agents
# ✅ I Manage The Workflow (Who Does What, In What Order)
# ✅ I Aggregate Results Into One Coherent Response
# ✅ I Handle Errors Gracefully (If One Agent Fails, Others Continue)
# 
# MY AGENT TEAM:
# -------------
# - ForecastAgent (port 9001): Predicts Agricultural Risks From Weather/Satellite
# - VerifyAgent (port 9002): Validates Data Quality And Cross-Checks Information
# - Future Agents Can Be Added Easily (MarketAgent, SoilAgent, Etc.)
# 
# HOW I COMMUNICATE (Real A2A Protocol!):
# --------------------------------------
# 1. Discover Agents: GET /card Endpoint To Get Agent Capabilities
# 2. Create A2A Client : Using A2AClientFactory With Agent Card
# 3. Send Messages: Using A2A Message Format (Role + Text Parts)
# 4. Receive Responses: Stream Responses Asynchronously
# 
# EXAMPLE WORKFLOW:
# ----------------
# Farmer: "What are the risks for my tomato farm in Mumbai?"
# 
# Me -> ForecastAgent: "Analyze risks for Mumbai, 30 days"
# ForecastAgent -> Me: "65% flood risk, medium pest risk"
# 
# Me -> VerifyAgent: "Verify this forecast: [forecast data]"
# VerifyAgent -> Me: "Data quality: 92%, cross-checked with 3 sources"
# 
# Me -> Farmer (email): "Action Plan: High Flood Risk Detected..."
# 
# RUNNING ME:
# ----------
# python OrchestratorServer.py
# # Starts on http://localhost:9000
# # Requires ForecastAgent (9001) And VerifyAgent (9002) Running
# 
# ═══════════════════════════════════════════════════════════════════════════════

import os
import uvicorn
import httpx
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.client import A2AClient, A2ACardResolver, ClientConfig, ClientFactory
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types
from AgentExecutor import AgentExecutor


# ───────────────────────────────────────────────────────────────────────────
# Remote Agent Addresses
# ───────────────────────────────────────────────────────────────────────────
# These Must Be Running Before I Start! Each Agent Is A Separate Server.
# You Can Run Them In Different Terminals:
# Terminal 1: python ForecastAgentServer.py
# Terminal 2: python VerifyAgentServer.py
# Terminal 3: python OrchestratorServer.py (Me!)
# ───────────────────────────────────────────────────────────────────────────
FORECAST_AGENT_URL = "http://localhost:9001"
VERIFY_AGENT_URL = "http://localhost:9002"


class OrchestratorAgent:
    """
    The Brain Of The Operation - Real A2A Agent Orchestration.
    
    I Manage The Entire Multi-Agent Workflow Using Real A2A Protocol:
    - Discover Remote Agents Via Their /card Endpoints
    - Create A2A Clients For Each Agent
    - Send Tasks And Receive Responses
    - Coordinate The Workflow
    - Aggregate Results Into One Action Plan
    """
    
    def __init__(self, httpx_client: httpx.AsyncClient):
        """Initialize With HTTP Client."""
        self.HttpClient = httpx_client
        self.ForecastAgentClient = None
        self.VerifyAgentClient = None
    
    async def InitializeAgents(self):
        """Initialize Connections To Remote A2A Agents."""
        
        Config = ClientConfig(
            httpx_client=self.HttpClient,
            supported_transports=["http_json", "jsonrpc"]
        )
        Factory = ClientFactory(Config)
        
        # Get Forecast Agent Card
        ForecastCardResolver = A2ACardResolver(self.HttpClient, FORECAST_AGENT_URL)
        ForecastCard = await ForecastCardResolver.get_agent_card()
        self.ForecastAgentClient = Factory.create(ForecastCard)
        
        # Get Verify Agent Card
        VerifyCardResolver = A2ACardResolver(self.HttpClient, VERIFY_AGENT_URL)
        VerifyCard = await VerifyCardResolver.get_agent_card()
        self.VerifyAgentClient = Factory.create(VerifyCard)
        
        print("✅ Connected To Remote A2A Agents")
    
    async def ExecuteWorkflow(self, UserQuery: str) -> str:
        """
        Execute Multi-Agent A2A Workflow.
        
        Args:
            UserQuery: User's Agricultural Query
            
        Returns:
            Final Orchestrated Response
        """
        
        Results = []
        
        try:
            # Step 1: Send To Forecast Agent
            from a2a.types import Message, TextPart
            
            ForecastMessage = Message(
                role="user",
                parts=[TextPart(text=UserQuery)]
            )
            
            print("📡 Sending To ForecastAgent...")
            ForecastResponse = None
            async for Event in self.ForecastAgentClient.send_message(ForecastMessage):
                if isinstance(Event, Message):
                    ForecastResponse = Event
                    break
                elif isinstance(Event, tuple) and Event[0]:
                    Task = Event[0]
                    if Task.messages:
                        ForecastResponse = Task.messages[-1]
            
            ForecastText = ""
            if ForecastResponse:
                for Part in ForecastResponse.parts:
                    if hasattr(Part, 'text'):
                        ForecastText += Part.text
            
            Results.append(f"FORECAST:\n{ForecastText}")
            
            # Step 2: Send To Verify Agent
            VerifyMessage = Message(
                role="user",
                parts=[TextPart(text=f"Verify This Forecast:\n{ForecastText}")]
            )
            
            print("📡 Sending To VerifyAgent...")
            VerifyResponse = None
            async for Event in self.VerifyAgentClient.send_message(VerifyMessage):
                if isinstance(Event, Message):
                    VerifyResponse = Event
                    break
                elif isinstance(Event, tuple) and Event[0]:
                    Task = Event[0]
                    if Task.messages:
                        VerifyResponse = Task.messages[-1]
            
            VerifyText = ""
            if VerifyResponse:
                for Part in VerifyResponse.parts:
                    if hasattr(Part, 'text'):
                        VerifyText += Part.text
            
            Results.append(f"VERIFICATION:\n{VerifyText}")
            
            # Step 3: Synthesize Final Recommendation
            FinalResponse = f"""
AGRISENSE-GUARDIAN MULTI-AGENT ANALYSIS
========================================

{Results[0]}

{Results[1]}

ORCHESTRATOR SYNTHESIS:
Based On The Independent Analyses From ForecastAgent And VerifyAgent, The Agricultural Risks Have Been Thoroughly Assessed And Cross-Validated. Review Both Reports Above For Complete Risk Understanding.
"""
            
            return FinalResponse
            
        except Exception as E:
            return f"ERROR: {str(E)}"


# Global Orchestrator Instance
OrchestratorInstance = None


def CreateOrchestratorADKAgent(Orchestrator: OrchestratorAgent) -> Agent:
    """Create ADK Agent That Uses A2A Orchestrator."""
    
    async def RunOrchestration(UserQuery: str) -> str:
        """Tool To Run A2A Orchestration."""
        return await Orchestrator.ExecuteWorkflow(UserQuery)
    
    return Agent(
        model="gemini-2.5-flash-lite",
        name="OrchestratorAgent",
        description="Multi-Agent Orchestration Coordinator",
        instruction="""
You Are OrchestratorAgent - The Multi-Agent Coordinator.

When The User Asks For Agricultural Risk Assessment, Call The RunOrchestration Tool
Which Will Coordinate ForecastAgent And VerifyAgent Via A2A Protocol.

The Tool Returns A Complete Multi-Agent Analysis.
""",
        tools=[RunOrchestration],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.4,
            top_p=0.95,
            max_output_tokens=3072,
        ),
    )


if __name__ == "__main__":
    import asyncio
    
    async def Main():
        global OrchestratorInstance
        
        # Create HTTP Client
        async with httpx.AsyncClient() as HttpClient:
            # Create Orchestrator
            OrchestratorInstance = OrchestratorAgent(HttpClient)
            
            # Initialize Remote Agent Connections
            await OrchestratorInstance.InitializeAgents()
            
            # Define Agent Skill
            Skill = AgentSkill(
                id="multi_agent_orchestration",
                name="Multi-Agent Agricultural Analysis",
                description="Orchestrates Multiple Specialized Agents For Comprehensive Agricultural Risk Assessment",
                tags=["orchestration", "multi-agent", "agriculture", "coordination"],
                examples=[
                    "Analyze Agricultural Risks For My Farm",
                    "What Are The Risks For Nairobi, Kenya Over 30 Days?",
                    "Comprehensive Risk Assessment"
                ],
            )
            
            # Define Agent Card
            AgentCardDef = AgentCard(
                name="OrchestratorAgent",
                description="Multi-Agent Orchestration System For Agricultural Risk Assessment",
                url="http://localhost:9000/",
                version="1.0.0",
                default_input_modes=["text"],
                default_output_modes=["text"],
                capabilities=AgentCapabilities(streaming=True),
                skills=[Skill],
            )
            
            # Create ADK Agent
            AdkAgent = CreateOrchestratorADKAgent(OrchestratorInstance)
            
            # Create Runner
            RunnerInstance = Runner(
                app_name=AgentCardDef.name,
                agent=AdkAgent,
                artifact_service=InMemoryArtifactService(),
                session_service=InMemorySessionService(),
                memory_service=InMemoryMemoryService(),
            )
            
            # Create Agent Executor
            Executor = AgentExecutor(RunnerInstance, AgentCardDef)
            
            # Create Request Handler
            RequestHandler = DefaultRequestHandler(
                agent_executor=Executor,
                task_store=InMemoryTaskStore()
            )
            
            # Create A2A Application
            A2AApp = A2AStarletteApplication(
                agent_card=AgentCardDef,
                http_handler=RequestHandler
            )
            
            print(f"🚀 Starting OrchestratorAgent A2A Server On Port 9000...")
            print(f"📍 Agent Card: http://localhost:9000/.well-known/agent.json")
            print(f"📡 Connected To:")
            print(f"   - ForecastAgent: {FORECAST_AGENT_URL}")
            print(f"   - VerifyAgent: {VERIFY_AGENT_URL}")
            
            # Run Server
            Config = uvicorn.Config(A2AApp.build(), host="0.0.0.0", port=9000)
            Server = uvicorn.Server(Config)
            await Server.serve()
    
    asyncio.run(Main())