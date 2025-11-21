# AgriSenseGuardian Package Initialization
# Multi-Agent Agricultural Decision Support System

__version__ = "1.0.0"
__author__ = "AgriSenseGuardian Team"
__description__ = "Multi-Agent Agricultural Decision Support System Using Google ADK And A2A Patterns"

# Import Main Components For Easy Access
from .Agents import (
    OrchestratorAgent,
    ForecastAgent,
    VerifyAgent,
    PlannerAgent
)

from .Tools import (
    WeatherTool,
    GetSatelliteData,
    SatelliteFetchTool,
    CopernicusTool,
    EmailNotificationTool,
)

from .Utils import SetupLogger, AgentTelemetry

__all__ = [
    # Agents
    'OrchestratorAgent',
    'ForecastAgent',
    'VerifyAgent',
    'PlannerAgent',
    # Tools
    'WeatherTool',
    'GetSatelliteData',
    'SatelliteFetchTool',
    'CopernicusTool',
    'EmailNotificationTool',
    # Utilities
    'SetupLogger',
    'AgentTelemetry'
]
