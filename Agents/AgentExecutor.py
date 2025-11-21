# Real A2A Agent Executor With Session And Memory Management
# Required For A2A Server Integration

from a2a.server.executors import AgentExecutor as A2AAgentExecutor
from a2a.types import AgentCard, Message, Task, TaskState, TaskStatusUpdate
from google.adk.runners import Runner
import asyncio
from typing import AsyncIterator
import sys
sys.path.append('..')
from Utils.SessionManager import GlobalSessionManager


class AgentExecutor(A2AAgentExecutor):
    """
    Real A2A Agent Executor.
    
    Bridges ADK Runner With A2A Protocol.
    """
    
    def __init__(self, runner: Runner, agent_card: AgentCard):
        """Initialize Executor With ADK Runner."""
        self.Runner = runner
        self.AgentCard = agent_card
    
    async def execute(
        self,
        task: Task
    ) -> AsyncIterator[Task | TaskStatusUpdate]:
        """
        Execute Task Using ADK Runner With Session And Memory Management.
        
        Args:
            task: A2A Task To Execute
            
        Yields:
            Task Updates During Execution
        """
        
        # Update Task Status To Running
        task.status.state = TaskState.running
        yield task
        
        try:
            # Extract Message From Task
            if not task.messages:
                raise ValueError("No Messages In Task")
            
            LastMessage = task.messages[-1]
            UserQuery = ""
            
            for Part in LastMessage.parts:
                if hasattr(Part, 'text'):
                    UserQuery += Part.text
            
            # Session ID From Task
            SessionId = task.id
            
            # Create Or Get Session
            try:
                Session = await GlobalSessionManager.CreateSession(
                    SessionId=SessionId,
                    FarmerProfile={
                        'TaskId': task.id,
                        'AgentName': self.AgentCard.name
                    }
                )
            except:
                # Session May Already Exist
                pass
            
            # Update Session State With Query
            await GlobalSessionManager.UpdateSessionState(
                SessionId=SessionId,
                UpdateData={'Query': UserQuery}
            )
            
            # Recall Relevant Memories
            Memories = await GlobalSessionManager.RecallMemories(
                SessionId=SessionId,
                Query=UserQuery,
                TopK=3
            )
            
            # Build Context-Aware Query
            ContextualQuery = UserQuery
            if Memories:
                MemoryContext = "\n".join([
                    f"Previous Knowledge: {M.content}" for M in Memories[:2]
                ])
                ContextualQuery = f"{MemoryContext}\n\nCurrent Query: {UserQuery}"
            
            # Execute Using ADK Runner
            async for Event in self.Runner.run(
                query=ContextualQuery,
                session_id=SessionId
            ):
                # Stream Progress Updates
                if hasattr(Event, 'content'):
                    yield TaskStatusUpdate(
                        task_id=task.id,
                        state=TaskState.running,
                        message=str(Event.content)[:200]
                    )
            
            # Get Final Result
            FinalResult = await self.Runner.get_response(SessionId)
            
            # Store Result To Session State
            await GlobalSessionManager.UpdateSessionState(
                SessionId=SessionId,
                UpdateData={'RiskAssessment': str(FinalResult)}
            )
            
            # Store Important Information To Long-Term Memory
            await GlobalSessionManager.StoreToLongTermMemory(
                SessionId=SessionId,
                MemoryContent=f"Query: {UserQuery}\nResponse: {str(FinalResult)[:500]}",
                MemoryType="interaction_history"
            )
            
            # Create Response Message
            from a2a.types import TextPart
            ResponseMessage = Message(
                role="agent",
                parts=[TextPart(text=str(FinalResult))]
            )
            
            task.messages.append(ResponseMessage)
            task.status.state = TaskState.completed
            
            yield task
            
        except Exception as E:
            # Handle Errors
            task.status.state = TaskState.failed
            task.status.error = str(E)
            yield task