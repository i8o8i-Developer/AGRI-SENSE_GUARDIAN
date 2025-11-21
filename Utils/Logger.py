# AgriSenseGuardian Logger - Structured Logging And Telemetry Utility
# Implements ADK-Compliant Observability With Agent Metrics And Error Tracking
# Provides Configurable Logging To Console And Files With Performance Monitoring

import logging
import sys
from datetime import datetime
from typing import Optional


def SetupLogger(
    LoggerName: str = "AgriSenseGuardian",
    LogLevel: int = logging.INFO,
    LogToFile: bool = False,
    LogFilePath: Optional[str] = None
) -> logging.Logger:
    """
    Configure Application Logger With Structured Output And Multiple Handlers.
    
    Creates A Production-Ready Logger Instance With Consistent Formatting,
    Configurable Log Levels, And Optional File Output. Follows ADK Best Practices
    For Observability And Debugging In Multi-Agent Systems.
    
    Args:
        LoggerName: Identifier For The Logger Instance (Default: "AgriSenseGuardian")
        LogLevel: Minimum Logging Level Threshold (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        LogToFile: Enable File Logging In Addition To Console Output
        LogFilePath: Custom Path For Log File (Auto-Generated If Not Provided)
        
    Returns:
        logging.Logger: Configured Logger Instance Ready For Use Throughout Application
    """
    
    # Create Logger
    Logger = logging.getLogger(LoggerName)
    Logger.setLevel(LogLevel)
    
    # Avoid Duplicate Handlers
    if Logger.hasHandlers():
        Logger.handlers.clear()
    
    # Create Formatter
    Formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler
    ConsoleHandler = logging.StreamHandler(sys.stdout)
    ConsoleHandler.setLevel(LogLevel)
    ConsoleHandler.setFormatter(Formatter)
    Logger.addHandler(ConsoleHandler)
    
    # File Handler (Optional)
    if LogToFile:
        if not LogFilePath:
            LogFilePath = f"AgriSenseGuardian_{datetime.now().strftime('%Y%m%d')}.log"
        
        FileHandler = logging.FileHandler(LogFilePath, mode='a', encoding='utf-8')
        FileHandler.setLevel(LogLevel)
        FileHandler.setFormatter(Formatter)
        Logger.addHandler(FileHandler)
    
    return Logger


class AgentTelemetry:
    """
    Agent Execution Telemetry And Performance Metrics Collector.
    
    Tracks Comprehensive Metrics For Multi-Agent System Performance Including
    Execution Times, Tool Usage Patterns, Error Rates, And Session Statistics.
    Used For Monitoring System Health, Identifying Performance Bottlenecks,
    And Optimizing Agent Workflows.
    """
    
    def __init__(self):
        """
        Initialize Telemetry Collector With Empty Metrics Registry.
        
        Creates A New Telemetry Instance With Initialized Data Structures
        For Tracking Agent Performance, Tool Usage, And Error Patterns.
        """
        self.Metrics = {
            'AgentExecutions': {},
            'ToolCalls': {},
            'Errors': [],
            'SessionCount': 0
        }
    
    def RecordAgentExecution(self, AgentName: str, Duration: float, Status: str):
        """
        Record Metrics For A Completed Agent Execution.
        
        Updates Performance Statistics For The Specified Agent Including
        Execution Count, Total Duration, And Success/Error Rates.
        
        Args:
            AgentName: Name Of The Agent That Executed
            Duration: Execution Time In Seconds
            Status: Execution Result ('Success' Or Error Status)
        """
        if AgentName not in self.Metrics['AgentExecutions']:
            self.Metrics['AgentExecutions'][AgentName] = {
                'Count': 0,
                'TotalDuration': 0.0,
                'SuccessCount': 0,
                'ErrorCount': 0
            }
        
        self.Metrics['AgentExecutions'][AgentName]['Count'] += 1
        self.Metrics['AgentExecutions'][AgentName]['TotalDuration'] += Duration
        
        if Status == 'Success':
            self.Metrics['AgentExecutions'][AgentName]['SuccessCount'] += 1
        else:
            self.Metrics['AgentExecutions'][AgentName]['ErrorCount'] += 1
    
    def RecordToolCall(self, ToolName: str):
        """
        Record Usage Of A Specific Tool By Any Agent.
        
        Increments The Call Counter For The Specified Tool To Track
        Usage Patterns And Integration Frequency.
        
        Args:
            ToolName: Name Of The Tool That Was Called
        """
        if ToolName not in self.Metrics['ToolCalls']:
            self.Metrics['ToolCalls'][ToolName] = 0
        
        self.Metrics['ToolCalls'][ToolName] += 1
    
    def RecordError(self, ErrorMessage: str, AgentName: str):
        """
        Record An Error Event With Context Information.
        
        Logs Error Details Including Timestamp, Affected Agent, And
        Error Message For Debugging And Reliability Analysis.
        
        Args:
            ErrorMessage: Description Of The Error That Occurred
            AgentName: Name Of The Agent Where The Error Happened
        """
        self.Metrics['Errors'].append({
            'Timestamp': datetime.now().isoformat(),
            'Agent': AgentName,
            'Message': ErrorMessage
        })
    
    def GetMetricsSummary(self):
        """
        Generate Comprehensive Summary Of All Collected Telemetry Metrics.
        
        Compiles All Performance Data Into A Structured Summary Including
        Agent Execution Statistics, Tool Usage Counts, Error Totals, And
        Session Information For System Monitoring And Reporting.
        
        Returns:
            Dict: Complete Metrics Summary With All Tracked Performance Data
        """
        return {
            'AgentExecutions': self.Metrics['AgentExecutions'],
            'ToolCalls': self.Metrics['ToolCalls'],
            'ErrorCount': len(self.Metrics['Errors']),
            'SessionCount': self.Metrics['SessionCount']
        }