# AgriSenseGuardian Session Manager - Comprehensive Memory And Context Management
# Implements ADK Session And Memory Services For Multi-Agent Conversation Persistence
# Provides Short-Term Session State And Long-Term Memory Storage For Farmer Interactions

from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import InMemoryMemoryService
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class AgriSenseSessionManager:
    """
    Comprehensive Session And Memory Management For AgriSenseGuardian.
    
    Manages Both Short-Term Conversation State And Long-Term Memory Storage
    For Farmer Interactions. Tracks Farmer Profiles, Risk Assessments, Query
    History, And Recommendations Across Multiple Sessions Using ADK Services.
    
    Key Features:
    - Session State Persistence For Active Conversations
    - Long-Term Memory Storage For Cross-Session Knowledge
    - Farmer Profile And Preference Tracking
    - Risk Assessment History And Learning
    - Contextual Information Retrieval For Agents
    - Automatic Memory Compaction For LLM Context Limits
    """
    
    def __init__(self, app_name: str = "AgriSenseGuardian", user_id: str = "farmer"):
        """
        Initialize Session And Memory Services With ADK Integration.
        
        Creates In-Memory Session And Memory Services Following ADK Patterns,
        Ready For Production Scaling To Database-Backed Storage.
        
        Args:
            app_name: Application Identifier For ADK Services
            user_id: Default User Identifier For Sessions
        """
        self.SessionService = InMemorySessionService()
        self.MemoryService = InMemoryMemoryService()
        self.app_name = app_name
        self.user_id = user_id
        
        # Track Active Sessions
        self.ActiveSessions: Dict[str, Session] = {}
    
    async def CreateSession(
        self,
        SessionId: str,
        FarmerProfile: Dict[str, Any] = None
    ) -> Session:
        """
        Create New Session With Initial Farmer Profile And Context.
        
        Initializes A New Conversation Session With Farmer Information,
        Setting Up The Foundation For Context-Aware Agent Interactions.
        
        Args:
            SessionId: Unique Identifier For The Session
            FarmerProfile: Dictionary Containing Farmer Information Including
                          Name, Location, Crops, Farm Size, And Contact Details
            
        Returns:
            Session: ADK Session Object With Initialized State
            
        Raises:
            Exception: If Session Creation Fails Due To ADK Service Issues
        """
    
    def __init__(self, app_name: str = "AgriSenseGuardian", user_id: str = "farmer"):
        """Initialize Session And Memory Services."""
        self.SessionService = InMemorySessionService()
        self.MemoryService = InMemoryMemoryService()
        self.app_name = app_name
        self.user_id = user_id
        
        # Track Active Sessions
        self.ActiveSessions: Dict[str, Session] = {}
    
    async def CreateSession(
        self,
        SessionId: str,
        FarmerProfile: Dict[str, Any] = None
    ) -> Session:
        """
        Create New Session With Initial State.
        
        Args:
            SessionId: Unique Session Identifier
            FarmerProfile: Optional Farmer Information
            
        Returns:
            Session Object
        """
        
        # Initialize Session State
        InitialState = {
            'SessionId': SessionId,
            'CreatedAt': datetime.now().isoformat(),
            'FarmerProfile': FarmerProfile or {},
            'QueryHistory': [],
            'RiskAssessments': [],
            'Recommendations': [],
            'ConversationContext': {
                'Location': FarmerProfile.get('Location') if FarmerProfile else None,
                'CropType': FarmerProfile.get('CropType') if FarmerProfile else None,
                'FarmSize': FarmerProfile.get('FarmSize') if FarmerProfile else None
            }
        }
        
        # Create Session
        SessionObj = await self.SessionService.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=SessionId
        )
        
        # Set Initial State
        SessionObj.state = InitialState
        
        self.ActiveSessions[SessionId] = SessionObj
        
        print(f"📝 Session Created: {SessionId}")
        return SessionObj
    
    async def UpdateSessionState(
        self,
        SessionId: str,
        UpdateData: Dict[str, Any]
    ) -> Session:
        """
        Update Session State With New Information And Maintain History.
        
        Merges New Data Into The Existing Session State While Maintaining
        Historical Records Of Queries, Risk Assessments, And Recommendations.
        Automatically Timestamps All Historical Entries For Audit Trails.
        
        Args:
            SessionId: Unique Identifier Of The Session To Update
            UpdateData: Dictionary Containing Data To Add To Session State.
                       Special Keys Like 'Query', 'RiskAssessment', 'Recommendation'
                       Are Automatically Appended To History Arrays.
            
        Returns:
            Session: Updated ADK Session Object With New State
            
        Raises:
            ValueError: If Specified Session Does Not Exist
        """
        
        # Get Current Session
        CurrentSession = await self.SessionService.get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=SessionId
        )
        
        if not CurrentSession:
            raise ValueError(f"Session Not Found: {SessionId}")
        
        # Merge Update Data
        CurrentState = CurrentSession.state or {}
        
        # Append To History Arrays
        if 'Query' in UpdateData:
            if 'QueryHistory' not in CurrentState:
                CurrentState['QueryHistory'] = []
            CurrentState['QueryHistory'].append({
                'Timestamp': datetime.now().isoformat(),
                'Query': UpdateData['Query']
            })
        
        if 'RiskAssessment' in UpdateData:
            if 'RiskAssessments' not in CurrentState:
                CurrentState['RiskAssessments'] = []
            CurrentState['RiskAssessments'].append({
                'Timestamp': datetime.now().isoformat(),
                'Assessment': UpdateData['RiskAssessment']
            })
        
        if 'Recommendation' in UpdateData:
            if 'Recommendations' not in CurrentState:
                CurrentState['Recommendations'] = []
            CurrentState['Recommendations'].append({
                'Timestamp': datetime.now().isoformat(),
                'Recommendation': UpdateData['Recommendation']
            })
        
        # Update Other Fields
        for Key, Value in UpdateData.items():
            if Key not in ['Query', 'RiskAssessment', 'Recommendation']:
                CurrentState[Key] = Value
        
        # Save Updated State (Session State Is Automatically Persisted In InMemorySessionService)
        CurrentSession.state = CurrentState
        
        print(f"💾 Session Updated: {SessionId}")
        return CurrentSession
    
    async def StoreToLongTermMemory(
        self,
        SessionId: str,
        MemoryContent: str,
        MemoryType: str = "agricultural_knowledge"
    ) -> None:
        """
        Transfer Important Information To Long-Term Memory Storage.
        
        Stores Session Information In ADK Memory Service For Cross-Session
        Retrieval And Learning. Includes Farmer Profile Context And Location
        Information For Better Relevance Scoring.
        
        Args:
            SessionId: Source Session Identifier For Context Retrieval
            MemoryContent: Text Content To Store In Long-Term Memory
            MemoryType: Category Classification For Memory Organization
                       (e.g., 'risk_history', 'farmer_profile', 'session_archive')
        """
        
        # Get Session For Context
        SessionObj = await self.SessionService.get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=SessionId
        )
        
        if not SessionObj:
            raise ValueError(f"Session Not Found: {SessionId}")
        
        # Update Session State With The Memory Content And Metadata
        current_state = SessionObj.state or {}
        if 'memories' not in current_state:
            current_state['memories'] = []
        
        current_state['memories'].append({
            'Type': MemoryType,
            'Content': MemoryContent,
            'Timestamp': datetime.now().isoformat(),
            'FarmerProfile': current_state.get('FarmerProfile', {}),
            'Location': current_state.get('ConversationContext', {}).get('Location')
        })
        
        # Store Session To Memory Using ADK's add_session_to_memory
        await self.MemoryService.add_session_to_memory(SessionObj)
        
        print(f"🧠 Stored To Long-Term Memory: {MemoryType}")
    
    async def RecallMemories(
        self,
        SessionId: str,
        Query: str,
        TopK: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve Relevant Memories From Long-Term Storage Using Semantic Search.
        
        Searches The ADK Memory Service For Information Relevant To The Query,
        Returning The Most Similar Memories Based On Content And Context Matching.
        
        Args:
            SessionId: Current Session Identifier For User Context
            Query: Natural Language Search Query For Memory Retrieval
            TopK: Maximum Number Of Memories To Return (Default: 5)
            
        Returns:
            List[Dict[str, Any]]: List Of Relevant Memory Objects With Metadata
        """
        
        # Search Memory Service Using The Correct ADK API
        SearchResponse = await self.MemoryService.search_memory(
            app_name="AgriSenseGuardian",
            user_id=SessionId,
            query=Query
        )
        
        # Extract Memories From Response
        Memories = SearchResponse.memories if hasattr(SearchResponse, 'memories') else []
        
        print(f"🔍 Retrieved {len(Memories)} Memories For: {Query[:50]}...")
        return Memories[:TopK]  # Limit To TopK Results
    
    async def GetConversationContext(
        self,
        SessionId: str
    ) -> Dict[str, Any]:
        """
        Get Complete Conversation Context Including Session State And Recent Memories.
        
        Retrieves All Available Context For A Session Including Current State,
        Recent Memories, And Activity Statistics For Agent Decision Making.
        
        Args:
            SessionId: Session Identifier To Retrieve Context For
            
        Returns:
            Dict[str, Any]: Complete Context Dictionary With Session State,
                           Recent Memories, Query Count, And Last Activity Timestamp
        """
        
        # Get Session State
        SessionObj = await self.SessionService.get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=SessionId
        )
        
        if not SessionObj:
            return {'Error': 'Session Not Found'}
        
        # Build Context (Memories Are Stored In Session State, Not Separately)
        Context = {
            'SessionId': SessionId,
            'SessionState': SessionObj.state,
            'RecentMemories': SessionObj.state.get('memories', [])[-10:] if SessionObj.state.get('memories') else [],
            'QueryCount': len(SessionObj.state.get('QueryHistory', [])),
            'LastActivity': SessionObj.state.get('QueryHistory', [{}])[-1].get('Timestamp') if SessionObj.state.get('QueryHistory') else None
        }
        
        return Context
    
    async def CompactContext(
        self,
        SessionId: str,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """
        Create A Compact Snapshot Of The Session Context Suitable For LLM Prompts.

        Heuristics:
        - Keep Last N Items Of QueryHistory, RiskAssessments, Recommendations
        - Trim Large Fields And Drop Non-Essential Debug Fields
        - Approximate Tokens As Chars/4 And Reduce Until Under Max_Tokens

        Returns Compact Dict And Also Stores Summary Metadata In Session State.
        """
        Context = await self.GetConversationContext(SessionId)
        State = dict(Context.get('SessionState') or {})

        def _trim_list(lst, keep=5):
            if not isinstance(lst, list):
                return lst
            return lst[-keep:]

        # Start With A Compact Structure
        compact = {
            'SessionId': SessionId,
            'FarmerProfile': State.get('FarmerProfile', {}),
            'ConversationContext': State.get('ConversationContext', {}),
            'QueryHistory': _trim_list(State.get('QueryHistory', []), keep=5),
            'RiskAssessments': _trim_list(State.get('RiskAssessments', []), keep=3),
            'Recommendations': _trim_list(State.get('Recommendations', []), keep=3),
            'RecentMemories': _trim_list(Context.get('RecentMemories', []), keep=3)
        }

        import json
        def est_tokens(obj) -> int:
            try:
                s = json.dumps(obj, ensure_ascii=False)
            except Exception:
                s = str(obj)
            return max(1, len(s) // 4)

        # Iteratively Trim Until Within Token Budget
        keep_q = 5
        keep_risk = 3
        keep_rec = 3
        keep_mem = 3

        while est_tokens(compact) > max_tokens and any(k > 1 for k in [keep_q, keep_risk, keep_rec, keep_mem]):
            if keep_q > 1:
                keep_q -= 1
            elif keep_risk > 1:
                keep_risk -= 1
            elif keep_rec > 1:
                keep_rec -= 1
            elif keep_mem > 1:
                keep_mem -= 1
            compact['QueryHistory'] = _trim_list(State.get('QueryHistory', []), keep=keep_q)
            compact['RiskAssessments'] = _trim_list(State.get('RiskAssessments', []), keep=keep_risk)
            compact['Recommendations'] = _trim_list(State.get('Recommendations', []), keep=keep_rec)
            compact['RecentMemories'] = _trim_list(Context.get('RecentMemories', []), keep=keep_mem)

        # Store A Brief Summary Back Into Session State
        summary = {
            'Counts': {
                'Queries': len(State.get('QueryHistory', [])),
                'Risks': len(State.get('RiskAssessments', [])),
                'Recs': len(State.get('Recommendations', []))
            },
            'Kept': {
                'Queries': len(compact['QueryHistory']),
                'Risks': len(compact['RiskAssessments']),
                'Recs': len(compact['Recommendations']),
                'Memories': len(compact['RecentMemories'])
            },
            'EstimatedTokens': est_tokens(compact)
        }

        await self.UpdateSessionState(SessionId, {'CompactContextSummary': summary})
        return compact

    async def StoreFarmerKnowledge(
        self,
        SessionId: str,
        Knowledge: Dict[str, Any]
    ):
        """
        Store Farmer-Specific Knowledge To Memory.
        
        Examples:
        - Crop preferences
        - Past risk experiences
        - Successful mitigation strategies
        - Location-specific observations
        """
        
        # Format Knowledge For Storage
        KnowledgeText = json.dumps(Knowledge, indent=2)
        
        await self.StoreToLongTermMemory(
            SessionId=SessionId,
            MemoryContent=f"Farmer Knowledge: {KnowledgeText}",
            MemoryType="farmer_profile"
        )
    
    async def StoreRiskHistory(
        self,
        SessionId: str,
        RiskAssessment: Dict[str, Any],
        ActualOutcome: Optional[str] = None
    ):
        """
        Store Risk Assessment And Outcomes For Learning.
        
        This Enables:
        - Prediction accuracy tracking
        - Pattern recognition
        - Personalized recommendations
        """
        
        HistoryEntry = {
            'Assessment': RiskAssessment,
            'Timestamp': datetime.now().isoformat(),
            'ActualOutcome': ActualOutcome
        }
        
        await self.StoreToLongTermMemory(
            SessionId=SessionId,
            MemoryContent=f"Risk History: {json.dumps(HistoryEntry)}",
            MemoryType="risk_history"
        )
    
    async def GetSessionSummary(
        self,
        SessionId: str
    ) -> str:
        """
        Generate Human-Readable Session Summary.
        
        Returns:
            Summary String
        """
        
        Context = await self.GetConversationContext(SessionId)
        
        SessionState = Context.get('SessionState', {})
        
        Summary = f"""
SESSION SUMMARY
===============
Session ID: {SessionId}
Created: {SessionState.get('CreatedAt', 'N/A')}
Last Activity: {Context.get('LastActivity', 'N/A')}

FARMER PROFILE:
{json.dumps(SessionState.get('FarmerProfile', {}), indent=2)}

CONVERSATION STATS:
- Total Queries: {Context.get('QueryCount', 0)}
- Risk Assessments: {len(SessionState.get('RiskAssessments', []))}
- Recommendations Provided: {len(SessionState.get('Recommendations', []))}

RECENT MEMORIES:
{len(Context.get('RecentMemories', []))} memories stored

CONVERSATION CONTEXT:
Location: {SessionState.get('ConversationContext', {}).get('Location', 'Not specified')}
Crop Type: {SessionState.get('ConversationContext', {}).get('CropType', 'Not specified')}
Farm Size: {SessionState.get('ConversationContext', {}).get('FarmSize', 'Not specified')}
"""
        
        return Summary
    
    async def CloseSession(
        self,
        SessionId: str,
        ConsolidateMemories: bool = True
    ):
        """
        Close Session And Optionally Consolidate To Long-Term Memory.
        
        Args:
            SessionId: Session To Close
            ConsolidateMemories: If True, Store Session Summary To Memory
        """
        
        if ConsolidateMemories:
            # Get Session Summary
            Summary = await self.GetSessionSummary(SessionId)
            
            # Store To Long-Term Memory
            await self.StoreToLongTermMemory(
                SessionId=SessionId,
                MemoryContent=f"Session Summary:\n{Summary}",
                MemoryType="session_archive"
            )
        
        # Remove From Active Sessions
        if SessionId in self.ActiveSessions:
            del self.ActiveSessions[SessionId]
        
        print(f"🔒 Session Closed: {SessionId}")


# Global Session Manager Instance
GlobalSessionManager = AgriSenseSessionManager()