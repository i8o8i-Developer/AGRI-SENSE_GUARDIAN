from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Callable, Awaitable


@dataclass
class TaskRecord:
    id: str
    status: str = "Pending"  # Pending | Running | Paused | Completed | Error | Cancelled
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    paused: bool = False
    pause_event: asyncio.Event = field(default_factory=asyncio.Event)
    coro: Optional[asyncio.Task] = None


class TaskManager:
    """
    Asynchronous Task Execution Manager With Pause/Resume Support.
    
    Manages The Lifecycle Of Long-Running Agricultural Analysis Tasks Including
    Multi-Agent Orchestration, Risk Assessment Workflows, And Complex Data Processing.
    Provides Thread-Safe Operations With Comprehensive Status Tracking And Control.
    """
    def __init__(self):
        """
        Initialize Task Manager With Empty Task Registry.
        
        Creates A New Task Manager Instance With Async Lock For Thread-Safe Operations
        And Empty Task Dictionary For Storing Active Task Records.
        """
        self._tasks: Dict[str, TaskRecord] = {}
        self._lock = asyncio.Lock()

    def _new_id(self) -> str:
        """
        Generate Unique Task Identifier.
        
        Returns:
            str: UUID4-Based Unique Task Identifier String
        """
        return str(uuid.uuid4())

    async def start(self, runner: Callable[[str], Awaitable[Dict[str, Any]]]) -> str:
        """
        Start A New Asynchronous Task With The Provided Runner Function.
        
        Creates A New Task Record, Initializes Pause/Resume Control, And Starts
        The Task Execution In A Separate Async Context With Proper Error Handling.
        
        Args:
            runner: Async Callable That Takes Task ID And Returns Result Dict
            
        Returns:
            str: Unique Task Identifier For Status Monitoring And Control
        """
        async with self._lock:
            task_id = self._new_id()
            record = TaskRecord(id=task_id)
            record.pause_event.set()  
            self._tasks[task_id] = record

            async def _wrap():
                record.status = "Running"
                try:
                    result = await runner(task_id)
                    record.result = result
                    record.status = "Completed"
                except asyncio.CancelledError:
                    record.status = "Cancelled"
                except Exception as e:
                    record.error = str(e)
                    record.status = "Error"

            record.coro = asyncio.create_task(_wrap(), name=f"AgriTask:{task_id}")
            return task_id

    async def pause(self, task_id: str) -> Dict[str, Any]:
        """
        Pause Execution Of A Running Task.
        
        Sets The Task's Pause Flag And Clears The Pause Event To Halt Execution
        At The Next Pause Check Point. The Task Will Remain In Paused State Until
        Explicitly Resumed.
        
        Args:
            task_id: Unique Task Identifier To Pause
            
        Returns:
            Dict: Pause Operation Result With Status And Task State Information
        """
        rec = self._tasks.get(task_id)
        if not rec:
            return {"Status": "Error", "Message": "Task Not Found"}
        rec.paused = True
        rec.pause_event.clear()
        rec.status = "Paused"
        return {"Status": "Success", "TaskId": task_id, "State": rec.status}

    async def resume(self, task_id: str) -> Dict[str, Any]:
        """
        Resume Execution Of A Paused Task.
        
        Clears The Pause Flag And Sets The Pause Event To Allow Task Execution
        To Continue From The Point Where It Was Paused.
        
        Args:
            task_id: Unique Task Identifier To Resume
            
        Returns:
            Dict: Resume Operation Result With Status And Task State Information
        """
        rec = self._tasks.get(task_id)
        if not rec:
            return {"Status": "Error", "Message": "Task Not Found"}
        rec.paused = False
        rec.pause_event.set()
        if rec.coro and not rec.coro.done():
            rec.status = "Running"
        return {"Status": "Success", "TaskId": task_id, "State": rec.status}

    async def cancel(self, task_id: str) -> Dict[str, Any]:
        """
        Cancel Execution Of A Running Or Paused Task.
        
        Sends Cancellation Signal To The Task Coroutine And Updates Task Status
        To Cancelled. The Task Will Stop Execution At The Next Cancellation Check.
        
        Args:
            task_id: Unique Task Identifier To Cancel
            
        Returns:
            Dict: Cancel Operation Result With Status And Task State Information
        """
        rec = self._tasks.get(task_id)
        if not rec:
            return {"Status": "Error", "Message": "Task Not Found"}
        if rec.coro and not rec.coro.done():
            rec.coro.cancel()
        rec.status = "Cancelled"
        return {"Status": "Success", "TaskId": task_id, "State": rec.status}

    def status(self, task_id: str) -> Dict[str, Any]:
        """
        Get Current Status And Details Of A Task.
        
        Retrieves Complete Task Information Including Current State, Results,
        Errors, And Pause Status. Used For Monitoring Task Progress And State.
        
        Args:
            task_id: Unique Task Identifier To Query
            
        Returns:
            Dict: Task Status Information With Complete Task Record Details
        """
        rec = self._tasks.get(task_id)
        if not rec:
            return {"Status": "Error", "Message": "Task Not Found"}
        return {
            "Status": "Success",
            "Task": {
                "Id": rec.id,
                "State": rec.status,
                "Paused": rec.paused,
                "Result": rec.result,
                "Error": rec.error
            }
        }

    async def wait_if_paused(self, task_id: str):
        """
        Pause Execution Point For Pause/Resume Control.
        
        Called Within Task Execution To Check For Pause State. If Task Is Paused,
        This Method Will Wait Until The Task Is Resumed Before Continuing Execution.
        
        Args:
            task_id: Task Identifier To Check For Pause State
        """
        rec = self._tasks.get(task_id)
        if not rec:
            return
        # Wait Here If Paused; The Event Is Cleared When Paused
        await rec.pause_event.wait()


# Singleton Accessor
_manager: Optional[TaskManager] = None


def get_task_manager() -> TaskManager:
    global _manager
    if _manager is None:
        _manager = TaskManager()
    return _manager


__all__ = ["get_task_manager", "TaskManager"]