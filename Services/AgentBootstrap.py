from __future__ import annotations

import os
import sys
import time
import signal
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from Config.Settings import get_settings  # type: ignore


CREATE_NEW_CONSOLE = 0x00000010  # Windows Creation Flag


@dataclass
class _Proc:
    name: str
    script: Path
    port: int
    process: Optional[subprocess.Popen] = None


class AgentBootstrap:
    """
    Agent Server Bootstrap And Lifecycle Manager.
    
    Manages The Startup, Shutdown, And Monitoring Of A2A Agent Servers As Separate
    Processes. Each Agent (Orchestrator, Forecast, Verify) Runs In Its Own Process
    With Configured Ports And Environment Variables For Inter-Agent Communication.
    
    Provides Graceful Process Management With Proper Signal Handling, Timeout
    Controls, And Status Reporting For Operational Monitoring And Debugging.
    """

    def __init__(self):
        self.settings = get_settings()
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        agents_dir = os.path.join(base, "Agents")
        self._procs: Dict[str, _Proc] = {
            "orchestrator": _Proc("orchestrator", os.path.join(agents_dir, "OrchestratorServer.py"), self.settings.a2a_ports.orchestrator),
            "forecast": _Proc("forecast", os.path.join(agents_dir, "ForecastAgentServer.py"), self.settings.a2a_ports.forecast),
            "verify": _Proc("verify", os.path.join(agents_dir, "VerifyAgentServer.py"), self.settings.a2a_ports.verify),
        }
        self._cwd = str(base)

    def start_agent(self, name: str) -> bool:
        """
        Start A Specific Agent Server Process.
        
        Launches The Specified Agent Server In A New Process With Proper Environment
        Configuration. Creates A New Console Window On Windows For Independent Process
        Management. Includes Brief Startup Delay For Process Initialization.
        
        Args:
            name: Agent Name To Start ('orchestrator', 'forecast', Or 'verify')
            
        Returns:
            bool: True If Agent Started Successfully, False On Failure
            
        Raises:
            ValueError: If Agent Name Is Not Recognized
        """
        proc = self._procs.get(name)
        if not proc:
            raise ValueError(f"Unknown Agent: {name}")
        if proc.process and proc.process.poll() is None:
            return True  # already running

        env = os.environ.copy()
        env.setdefault("A2A_HOST", self.settings.a2a_host)
        env.setdefault("A2A_PORT", str(proc.port))

        cmd = [sys.executable, "-u", str(proc.script)]
        try:
            p = subprocess.Popen(
                cmd,
                cwd=self._cwd,
                env=env,
                creationflags=CREATE_NEW_CONSOLE if os.name == "nt" else 0,
            )
            proc.process = p
            time.sleep(0.5)
            return True
        except Exception:
            return False

    def stop_agent(self, name: str, timeout: float = 5.0) -> bool:
        """
        Stop A Specific Agent Server Process Gracefully.
        
        Sends Termination Signal To The Specified Agent Process And Waits For
        Graceful Shutdown. Falls Back To Force Kill If Process Doesn't Respond
        Within Timeout Period. Uses SIGTERM On Unix Systems And Terminate On Windows.
        
        Args:
            name: Agent Name To Stop ('orchestrator', 'forecast', Or 'verify')
            timeout: Maximum Time In Seconds To Wait For Graceful Shutdown
            
        Returns:
            bool: True If Agent Stopped Successfully, False On Failure
        """
        proc = self._procs.get(name)
        if not proc or not proc.process:
            return True
        p = proc.process
        if p.poll() is not None:
            proc.process = None
            return True

        try:
            if os.name == "nt":
                p.terminate()
            else:
                p.send_signal(signal.SIGTERM)
            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                p.kill()
            finally:
                proc.process = None
            return True
        except Exception:
            return False

    def start_all(self) -> Dict[str, bool]:
        """
        Start All Configured Agent Server Processes.
        
        Attempts To Start All Agent Servers (Orchestrator, Forecast, Verify)
        In Sequence. Returns Status For Each Agent Individually.
        
        Returns:
            Dict[str, bool]: Dictionary Mapping Agent Names To Startup Success Status
        """
        return {name: self.start_agent(name) for name in self._procs.keys()}

    def stop_all(self) -> Dict[str, bool]:
        """
        Stop All Running Agent Server Processes.
        
        Attempts To Stop All Currently Running Agent Servers With Graceful
        Shutdown. Returns Status For Each Agent Individually.
        
        Returns:
            Dict[str, bool]: Dictionary Mapping Agent Names To Shutdown Success Status
        """
        return {name: self.stop_agent(name) for name in list(self._procs.keys())}

    def status(self) -> Dict[str, str]:
        """
        Get Current Status Of All Agent Server Processes.
        
        Checks The Running State Of Each Agent Server And Reports Current
        Status Including Host/Port Information For Running Processes.
        
        Returns:
            Dict[str, str]: Dictionary Mapping Agent Names To Status Strings
                           ('Running On host:port' Or 'Stopped')
        """
        status_info = {}
        running_count = 0
        total_count = len(self._procs)
        
        for name, proc in self._procs.items():
            if proc.process and proc.process.poll() is None:
                status_info[name] = f"Running on {self.settings.a2a_host}:{proc.port}"
                running_count += 1
            else:
                status_info[name] = "Stopped"
        
        return {
            'running_count': running_count,
            'total_count': total_count,
            'agents': status_info
        }

__all__ = ["AgentBootstrap"]