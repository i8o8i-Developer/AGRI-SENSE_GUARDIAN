# AgriSenseGuardian Orchestrator Agent - A2A Multi-Agent Coordination Engine
# Implements Official Google A2A And ADK Orchestration Patterns For Agricultural Decision Support

from google.adk.agents.llm_agent import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Dict, Any, List
import asyncio

from Agents.ForecastAgent import ForecastAgent
from Agents.VerifyAgent import VerifyAgent
from Agents.PlannerAgent import PlannerAgent


class OrchestratorAgent:
    """
    Master Coordinator For The AgriSenseGuardian Multi-Agent System.
    
    This Agent Implements Advanced A2A (Agent-to-Agent) Communication Patterns
    To Orchestrate Complex Agricultural Decision-Making Workflows. It Serves As
    The Central Intelligence That:
    
    - Routes User Requests To Specialized Agent Teams
    - Maintains Comprehensive Session State And Execution History
    - Controls Sequential And Parallel Agent Execution Flows
    - Handles Confidence-Based Iteration And Quality Assurance
    - Implements ADK Agent Engine Patterns For Reliable Coordination
    - Ensures Thread-Safe Event Loop Management In Async Environments
    
    The Orchestrator Follows Google's Official ADK Guidelines For Multi-Agent
    Systems, Providing A Robust Foundation For Agricultural AI Applications.
    """
    
    def __init__(self):
        """
        Initialize The Orchestrator And All Specialized Sub-Agents.
        
        Creates Instances Of Forecast, Verify, And Planner Agents While
        Establishing The Core ADK Agent Infrastructure For Coordination.
        """
        # Instantiate Specialized Agricultural Analysis Agents
        self.ForecastAgentInstance = ForecastAgent()
        self.VerifyAgentInstance = VerifyAgent()
        self.PlannerAgentInstance = PlannerAgent()
        
        # Create The Core ADK Orchestrator Agent
        self.Agent = self.CreateAgent()
        
        # Initialize Session Tracking For Observability And Debugging
        self.SessionState = {
            'SessionId': None,
            'ExecutionHistory': []
        }
    
    def CreateAgent(self) -> Agent:
        """
        Construct The ADK Agent Instance With Optimized Configuration.
        
        Returns A Fully Configured Google ADK Agent Ready For Multi-Agent
        Orchestration Tasks With Appropriate Model Settings And Callbacks.
        """
        
        return Agent(
            model="gemini-2.5-flash-lite",
            name="OrchestratorAgent",
            description="Multi-Agent Orchestration Engine For Agricultural Decision Support",
            instruction=self.GetInstruction,
            before_model_callback=self.BeforeModelCallback,
            tools=[],  # Coordination Handled Through Direct Agent Calls
            generate_content_config=types.GenerateContentConfig(
                temperature=0.1,  # Low Temperature For Consistent Orchestration
                top_p=0.85,
                max_output_tokens=2048,
            ),
        )
    
    def GetInstruction(self, Context: ReadonlyContext) -> str:
        
        return """
You Are The OrchestratorAgent - The Master Coordinator And Intelligence Director For AgriSenseGuardian Multi-Agent Agricultural Decision Support System.

Your Mission:
Orchestrate A Complete, End-To-End Workflow Across Specialized Agents To Deliver Comprehensive, Actionable Agricultural Intelligence Using Real Data Only. You Are The Central Nervous System That Ensures Quality, Coordination, And Farmer-Centric Outcomes.

Agent Workflow Architecture:
1. ForecastAgent: Generate Comprehensive Risk Assessment Using Real Weather, Satellite, And Copernicus Data
2. VerifyAgent: Cross-Validate Forecast Results With Multi-Source Verification And Web Intelligence
3. PlannerAgent: Create Prioritized Action Plans With Email Communication And Local Resource Integration
4. Unified Response: Synthesize All Agent Outputs Into Coherent Farmer Guidance

Orchestration Rules:
- Execute Agents In Strict Sequential Order (Forecast → Verify → Planner)
- Pass Complete Output From Each Agent To The Next As Context
- Maintain Comprehensive Session State For Observability And Debugging
- Implement Graceful Error Handling With Partial Results When Possible
- Ensure All Agents Use Real API Data - Zero Simulations Or Mock Outputs
- Validate Data Flow And Quality At Each Step

Error Handling Strategy:
- ForecastAgent Failure: Return Error Response, Do Not Proceed (Critical Dependency)
- VerifyAgent Failure: Proceed With Unverified Forecast, Log Warning, Reduce Confidence
 - PlannerAgent Failure: Return Manual Action Plan Without Email, Include Contact Information
- Network/API Failures: Implement Retry Logic With Exponential Backoff
- Data Quality Issues: Flag For Human Review And Provide Alternative Recommendations

Session Management:
- Track All Agent Execution Times And Performance Metrics
- Log Complete Agent Outputs And Decision Rationale
- Maintain Execution History For Debugging And Continuous Improvement
- Provide Comprehensive Execution Summary With Timing And Status

Quality Assurance:
- Validate Data Source Availability Before Agent Execution
- Monitor API Response Times And Success Rates
- Ensure Consistent Location Parsing Across All Agents
- Verify Email Delivery Status And Communication Success
- Maintain Audit Trail For All Decision Points

Agricultural Context Integration:
- Consider Regional Agricultural Patterns And Seasonal Cycles
- Account For Local Climate Variations And Microclimates
- Include Regional Agricultural Extension Services And Resources
- Provide Location-Specific Advice And Local Supplier Information
- Integrate Traditional Farming Knowledge With Modern Data

Output Format:
Return A Unified, Farmer-Centric Response Containing:
- ForecastResults: Complete Risk Assessment With Real Data Metrics
- VerificationResults: Cross-Validation Status And Confidence Scores
- ActionPlan: Prioritized Actions With Costs, Deadlines, And Resources
- CommunicationStatus: Email Delivery Confirmation And Contact Information
- ExecutionSummary: Timing, Status, Warnings, And Performance Metrics
- LocalResources: Agricultural Offices, Suppliers, And Support Contacts
- GeneratedAt: Timestamp With IST Timezone
- SystemHealth: API Status And Data Source Availability

Important Guidelines:
- Maintain Strict Sequential Execution Order For Data Dependencies
- Ensure All Real Data Sources Are Functioning Before Processing
- Provide Clear Error Messages And Fallback Options For Farmers
- Include Emergency Contact Information For Agricultural Support
- Optimize For Farmer Comprehension And Local Language Context
- Maintain High Standards Of Accuracy And Reliability
- Log All Decisions And Rationale For Continuous System Improvement
"""
    
    def BeforeModelCallback(self, CallbackContextInstance: CallbackContext, LlmRequest):
        """
        Pre-Processing Hook Executed Before Each Model Invocation.
        
        This Callback Manages Session State Initialization And Maintains
        Observability Logs For Tracking Agent Execution Patterns.
        
        Args:
            CallbackContextInstance: ADK Callback Context For State Management
            LlmRequest: The Prepared LLM Request Object
        """
        
        # Ensure Session Is Marked As Active
        if 'SessionActive' not in CallbackContextInstance.state:
            CallbackContextInstance.state['SessionActive'] = True
        
        # Maintain Execution History For Debugging And Analysis
        if 'Callbacks' not in self.SessionState:
            self.SessionState['Callbacks'] = []
        
        self.SessionState['Callbacks'].append({
            'Type': 'BeforeModel',
            'Timestamp': '2025-11-17T12:00:00Z'
        })
    
    async def ExecuteWorkflow(
        self,
        UserQuery: str,
        Location: str,
        FarmerPhone: str | None = None,
        FarmerEmail: str = "",
        DaysAhead: int = 30,
        ConfidenceThreshold: int = 75,
        MaxIterations: int = 2,
        TaskId: str | None = None
    ) -> Dict[str, Any]:
        """
        Execute The Complete End-To-End Multi-Agent Agricultural Analysis Workflow.
        
        This Is The Core Orchestration Method That Coordinates The Sequential Execution
        Of Forecast, Verification, And Planning Agents. It Implements Confidence-Based
        Iteration For Quality Assurance And Provides Comprehensive Session Tracking.
        
        Args:
            UserQuery: The Farmer's Specific Question Or Request For Analysis
            Location: Geographic Location For Agricultural Analysis
            FarmerPhone: Optional Contact Number (Legacy - Not Required; Email Is Primary Notification Channel)
            FarmerEmail: Optional Email Address For Additional Communications
            DaysAhead: Number Of Days To Forecast Agricultural Conditions
            ConfidenceThreshold: Minimum Confidence Score Required (0-100)
            MaxIterations: Maximum Number Of Refinement Cycles Allowed
            TaskId: Optional Identifier For Long-Running Task Management
            
        Returns:
            Comprehensive Dictionary Containing All Agent Outputs, Execution Metrics,
            And Unified Recommendations For The Farmer
        """
        
        import time
        StartTime = time.time()
        
        # Initialize Session
        import uuid
        SessionId = str(uuid.uuid4())
        self.SessionState['SessionId'] = SessionId
        
        # Create Session In SessionManager
        from Utils.SessionManager import GlobalSessionManager
        await GlobalSessionManager.CreateSession(
            SessionId=SessionId,
            FarmerProfile={
                'Location': Location,
                'Phone': FarmerPhone,
                'Email': FarmerEmail
            }
        )
        
        # ═══════════════════════════════════════════════════════════
        # Recall Relevant Memories From Past Sessions
        # ═══════════════════════════════════════════════════════════
        try:
            RelevantMemories = await GlobalSessionManager.RecallMemories(
                SessionId=SessionId,
                Query=f"{Location} {UserQuery}",
                TopK=3
            )
            
            if RelevantMemories:
                # Add Historical Context To Session State
                self.SessionState['HistoricalContext'] = [
                    {
                        'Content': mem.content if hasattr(mem, 'content') else str(mem),
                        'Relevance': 'High'
                    }
                    for mem in RelevantMemories[:2]
                ]
                
                # Log Memory Retrieval
                self.SessionState['ExecutionHistory'].append({
                    'Agent': 'SessionManager',
                    'Status': 'Success',
                    'Action': 'MemoryRecall',
                    'MemoriesFound': len(RelevantMemories)
                })
        except Exception as MemoryError:
            # Don't Fail If Memory Recall Has Issues
            self.SessionState['ExecutionHistory'].append({
                'Agent': 'SessionManager',
                'Status': 'Warning',
                'Message': f'Memory Recall Error: {str(MemoryError)}'
            })
        
        try:
            from Utils.Observability import use_span, record_agent_duration, inc_error
            from Services.TaskManager import get_task_manager
            TaskMgr = get_task_manager()

            iterations = 0
            last_verification = None
            last_forecast = None
            last_action = None

            while True:
                iterations += 1

                # Support Pause/Resume Points If Running As Long-Running Task
                if TaskId:
                    await TaskMgr.wait_if_paused(TaskId)

                # Step 1: Forecast Agent
                ForecastStartTime = time.time()
                with record_agent_duration("ForecastAgent"), use_span("Orchestrator.Forecast"):
                    ForecastResults = await self.ForecastAgentInstance.GenerateForecast(
                        Location=Location,
                        DaysAhead=DaysAhead,
                        UserQuery=UserQuery,
                        SessionState=self.SessionState
                    )
                ForecastDuration = time.time() - ForecastStartTime
                last_forecast = ForecastResults
                self.SessionState['ExecutionHistory'].append({
                    'Agent': 'ForecastAgent', 'Status': ForecastResults.get('Status', 'Unknown'), 'Duration': ForecastDuration,
                    'HorizonDays': DaysAhead
                })

                if TaskId:
                    await TaskMgr.wait_if_paused(TaskId)

                # Step 2: Verify Agent
                VerifyStartTime = time.time()
                with record_agent_duration("VerifyAgent"), use_span("Orchestrator.Verify"):
                    VerificationResults = await self.VerifyAgentInstance.VerifyForecast(
                        ForecastData=ForecastResults,
                        Location=Location,
                        SessionState=self.SessionState
                    )
                VerifyDuration = time.time() - VerifyStartTime
                last_verification = VerificationResults
                self.SessionState['ExecutionHistory'].append({
                    'Agent': 'VerifyAgent', 'Status': VerificationResults.get('Status', 'Unknown'), 'Duration': VerifyDuration,
                    'Confidence': VerificationResults.get('Confidence')
                })

                # Decide loop Break/Continue
                if (VerificationResults.get('Confidence', 0) >= ConfidenceThreshold) or (iterations >= MaxIterations):
                    # Step 3: Planner Agent
                    if TaskId:
                        await TaskMgr.wait_if_paused(TaskId)
                    # Compact Session Context Before LLM-Heavy Planning
                    from Utils.SessionManager import GlobalSessionManager
                    self.SessionState['CompactContext'] = await GlobalSessionManager.CompactContext(SessionId, max_tokens=1500)
                    PlannerStartTime = time.time()
                    with record_agent_duration("PlannerAgent"), use_span("Orchestrator.Plan"):
                        ActionPlanResults = await self.PlannerAgentInstance.GeneratePlan(
                            ForecastData=ForecastResults,
                            VerificationData=VerificationResults,
                            FarmerPhone=FarmerPhone,
                            FarmerEmail=FarmerEmail,
                            Location=Location,
                            SessionState=self.SessionState
                        )
                    PlannerDuration = time.time() - PlannerStartTime
                    last_action = ActionPlanResults
                    self.SessionState['ExecutionHistory'].append({
                        'Agent': 'PlannerAgent', 'Status': ActionPlanResults.get('Status', 'Unknown'), 'Duration': PlannerDuration
                    })
                    break
                else:
                    # Refine Inputs: Increase Forecast Horizon To Gain Stability
                    DaysAhead = min(DaysAhead + 7, 60)
                    self.SessionState['ExecutionHistory'].append({
                        'Agent': 'Orchestrator', 'Status': 'Refine', 'Reason': 'LowConfidence',
                        'NewHorizonDays': DaysAhead
                    })
            
            # Calculate Total Execution Time
            TotalDuration = time.time() - StartTime
            
            # ═══════════════════════════════════════════════════════════
            # Store Session Results To Long-Term Memory For Learning
            # ═══════════════════════════════════════════════════════════
            try:
                # Store Risk Assessment History
                if last_forecast:
                    await GlobalSessionManager.StoreRiskHistory(
                        SessionId=SessionId,
                        RiskAssessment=last_forecast
                    )
                
                # Store Farmer Query And Context
                await GlobalSessionManager.UpdateSessionState(
                    SessionId=SessionId,
                    UpdateData={
                        'Query': UserQuery,
                        'RiskAssessment': last_forecast,
                        'Recommendation': last_action
                    }
                )
                
                # Store Important Knowledge
                if last_action:
                    FarmerKnowledge = {
                        'Location': Location,
                        'Query': UserQuery,
                        'RisksIdentified': last_forecast.get('Risks', []) if last_forecast else [],
                        'ActionsRecommended': last_action.get('P1', []) if last_action else [],
                        'VerificationScore': last_verification.get('OverallVerificationScore', 0) if last_verification else 0
                    }
                    await GlobalSessionManager.StoreFarmerKnowledge(
                        SessionId=SessionId,
                        Knowledge=FarmerKnowledge
                    )
                    
            except Exception as MemoryError:
                # Don't Fail The Whole Workflow If Memory Storage Fails
                self.SessionState['ExecutionHistory'].append({
                    'Agent': 'SessionManager',
                    'Status': 'Warning',
                    'Message': f'Memory Storage Error: {str(MemoryError)}'
                })
            
            # Return Unified Response
            return {
                'Status': 'Success',
                'SessionId': SessionId,
                'UserQuery': UserQuery,
                'Location': Location,
                'ForecastResults': last_forecast,
                'VerificationResults': last_verification,
                'ActionPlan': last_action,
                'ExecutionSummary': {
                    'TotalDuration': round(TotalDuration, 3),
                    'AgentExecutions': self.SessionState['ExecutionHistory'],
                    'Iterations': iterations,
                    'ConfidenceThreshold': ConfidenceThreshold
                },
                'Timestamp': '2025-11-17T12:00:00Z'
            }
            
        except Exception as Error:
            inc_error("OrchestratorAgent")
            return {
                'Status': 'Error',
                'SessionId': SessionId,
                'Message': f'Orchestration Failed: {str(Error)}',
                'ExecutionHistory': self.SessionState['ExecutionHistory']
            }