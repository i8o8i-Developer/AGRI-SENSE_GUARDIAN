from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import httpx

# Local settings loader — Use Absolute Path Inside Project
from Config.Settings import get_settings  # type: ignore


@dataclass(frozen=True)
class AgentHealth:
    name: str
    host: str
    port: int
    port_open: bool
    http_status: Optional[int]


class HealthService:
    """
    Multi-Agent System Health Monitoring Service.
    
    Performs Automated Health Checks On All A2A Agent Servers And The Main API.
    Checks Network Port Availability And Optional HTTP Endpoint Responsiveness
    To Determine System Health And Readiness For Production Traffic.
    
    Used By Load Balancers, Monitoring Systems, And Deployment Pipelines To
    Verify System Operational Status And Detect Service Degradation.
    """

    def __init__(self, host: Optional[str] = None):
        """
        Initialize Health Service With Target Host Configuration.
        
        Args:
            host: Target Host For Health Checks (Defaults To A2A Host From Settings)
        """
        settings = get_settings()
        self.host = host or settings.a2a_host
        self.ports = settings.a2a_ports

    @staticmethod
    def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
        """
        Check If Network Port Is Open And Accepting Connections.
        
        Performs A TCP Socket Connection Test To Verify That The Specified
        Port Is Open And Responding To Connection Attempts.
        
        Args:
            host: Target Hostname Or IP Address
            port: Port Number To Test
            timeout: Connection Timeout In Seconds
            
        Returns:
            bool: True If Port Is Open And Accepting Connections
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False

    @staticmethod
    def _check_http(url: str, timeout: float = 2.0) -> Tuple[bool, Optional[int]]:
        """
        Perform HTTP Health Check On Endpoint.
        
        Makes An HTTP GET Request To The Specified URL And Returns Success
        Status And Response Code. Considers 5xx Errors As Unhealthy.
        
        Args:
            url: Full HTTP URL To Check (Including Protocol And Port)
            timeout: Request Timeout In Seconds
            
        Returns:
            Tuple[bool, Optional[int]]: (Success Status, HTTP Status Code)
        """
        try:
            with httpx.Client(timeout=timeout) as client:
                resp = client.get(url)
                return resp.status_code < 500, resp.status_code
        except Exception:
            return False, None

    def _build_agent_health(self, name: str, port: int, path_hint: str = "/") -> AgentHealth:
        """
        Build Comprehensive Health Check For Single Agent.
        
        Performs Both Port And HTTP Health Checks For An Individual Agent
        Server, Returning A Complete Health Status Descriptor.
        
        Args:
            name: Agent Name Identifier
            port: Agent Server Port Number
            path_hint: HTTP Path To Use For Health Check (Default: "/")
            
        Returns:
            AgentHealth: Complete Health Status For The Agent
        """
        host = self.host
        is_open = self._is_port_open(host, port)
        http_ok = None
        if is_open:
            ok, status = self._check_http(f"http://{host}:{port}{path_hint}")
            http_ok = status if ok else status
        return AgentHealth(name=name, host=host, port=port, port_open=is_open, http_status=http_ok)

    def check_a2a_agents(self) -> Dict[str, AgentHealth]:
        """
        Perform Health Checks On All A2A Agent Servers.
        
        Checks The Health Status Of All Configured Agent Servers (Orchestrator,
        Forecast, Verify) By Testing Port Availability And HTTP Responsiveness.
        
        Returns:
            Dict[str, AgentHealth]: Dictionary Mapping Agent Names To Health Status
        """
        results: Dict[str, AgentHealth] = {}
        results["orchestrator"] = self._build_agent_health("orchestrator", self.ports.orchestrator)
        results["forecast"] = self._build_agent_health("forecast", self.ports.forecast)
        results["verify"] = self._build_agent_health("verify", self.ports.verify)
        return results

    def readiness(self) -> Dict[str, object]:
        """
        Perform Complete System Readiness Assessment.
        
        Executes Comprehensive Health Checks Across All Agent Servers And
        Determines Overall System Readiness For Production Traffic. Used By
        Load Balancers And Deployment Systems For Automated Health Monitoring.
        
        Returns:
            Dict: Readiness Assessment With The Following Keys:
                - ready: Overall System Readiness Status (Boolean)
                - host: Target Host Being Checked
                - agents: Dictionary Of Individual Agent Health Statuses
        """
        agent_health = self.check_a2a_agents()
        all_healthy = all(agent.port_open for agent in agent_health.values())
        
        return {
            "ready": all_healthy,
            "host": self.host,
            "agents": {
                name: {
                    "port_open": agent.port_open,
                    "http_status": agent.http_status
                }
                for name, agent in agent_health.items()
            }
        }


__all__ = ["HealthService", "AgentHealth"]