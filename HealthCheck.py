#!/usr/bin/env python3
"""
🏥 AgriSenseGuardian Health Check Script
Comprehensive Health Monitoring For Container And Production Deployments
Validates All Critical System Components And Dependencies
"""

import asyncio
import sys
import time
from typing import Dict, Any, List
import logging

# Configure Basic Logging For Health Check
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
Logger = logging.getLogger(__name__)

async def CheckWebUIHealth() -> Dict[str, Any]:
    """
    Validate Web UI Endpoint Accessibility And Response Time.
    
    Returns:
        Dict: Health Status With Response Time And Status Code
    """
    try:
        import aiohttp
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as Session:
            StartTime = time.time()
            async with Session.get('http://localhost:8000/health') as Response:
                ResponseTime = (time.time() - StartTime) * 1000  # Convert To Milliseconds
                ResponseData = await Response.json()
                
                return {
                    'Status': 'Healthy' if Response.status == 200 else 'Unhealthy',
                    'StatusCode': Response.status,
                    'ResponseTime': round(ResponseTime, 2),
                    'Data': ResponseData
                }
    except Exception as E:
        return {
            'Status': 'Unhealthy',
            'Error': str(E),
            'ResponseTime': None
        }

async def CheckA2AAgentsHealth() -> Dict[str, Any]:
    """
    Validate A2A Agent Server Connectivity And Health Status.
    
    Returns:
        Dict: Comprehensive Agent Health Assessment
    """
    try:
        import aiohttp
        AgentPorts = [9000, 9001, 9002]  # Orchestrator, Forecast, Verify
        AgentNames = ['Orchestrator', 'Forecast', 'Verify']
        AgentResults = {}
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3)) as Session:
            for Name, Port in zip(AgentNames, AgentPorts):
                try:
                    StartTime = time.time()
                    async with Session.get(f'http://localhost:{Port}/health') as Response:
                        ResponseTime = (time.time() - StartTime) * 1000
                        AgentResults[Name] = {
                            'Status': 'Healthy' if Response.status == 200 else 'Unhealthy',
                            'Port': Port,
                            'StatusCode': Response.status,
                            'ResponseTime': round(ResponseTime, 2)
                        }
                except Exception as E:
                    AgentResults[Name] = {
                        'Status': 'Unhealthy',
                        'Port': Port,
                        'Error': str(E)
                    }
        
        HealthyCount = sum(1 for agent in AgentResults.values() if agent['Status'] == 'Healthy')
        TotalCount = len(AgentResults)
        
        return {
            'OverallStatus': 'Healthy' if HealthyCount == TotalCount else 'Degraded',
            'HealthyAgents': HealthyCount,
            'TotalAgents': TotalCount,
            'Agents': AgentResults
        }
        
    except Exception as E:
        return {
            'OverallStatus': 'Unhealthy',
            'Error': str(E)
        }

async def CheckSystemResources() -> Dict[str, Any]:
    """
    Monitor System Resource Utilization (CPU, Memory, Disk).
    
    Returns:
        Dict: System Resource Status And Usage Metrics
    """
    try:
        import psutil
        
        # CPU Usage
        CpuPercent = psutil.cpu_percent(interval=1)
        
        # Memory Usage
        Memory = psutil.virtual_memory()
        MemoryPercent = Memory.percent
        
        # Disk Usage
        Disk = psutil.disk_usage('/')
        DiskPercent = (Disk.used / Disk.total) * 100
        
        # Load Average (Unix-like systems)
        try:
            LoadAverage = psutil.getloadavg()[0]  # 1-minute load average
        except:
            LoadAverage = None
        
        # Determine Overall Resource Health
        ResourceStatus = 'Healthy'
        if CpuPercent > 80 or MemoryPercent > 85 or DiskPercent > 90:
            ResourceStatus = 'Warning'
        if CpuPercent > 95 or MemoryPercent > 95 or DiskPercent > 95:
            ResourceStatus = 'Critical'
        
        return {
            'Status': ResourceStatus,
            'CPU': {
                'UsagePercent': round(CpuPercent, 1),
                'LoadAverage': LoadAverage
            },
            'Memory': {
                'UsagePercent': round(MemoryPercent, 1),
                'Total': round(Memory.total / (1024**3), 2),  # GB
                'Available': round(Memory.available / (1024**3), 2)  # GB
            },
            'Disk': {
                'UsagePercent': round(DiskPercent, 1),
                'Total': round(Disk.total / (1024**3), 2),  # GB
                'Free': round(Disk.free / (1024**3), 2)  # GB
            }
        }
        
    except ImportError:
        return {
            'Status': 'Unknown',
            'Message': 'psutil Not Available - Install For Resource Monitoring'
        }
    except Exception as E:
        return {
            'Status': 'Error',
            'Error': str(E)
        }

async def CheckExternalDependencies() -> Dict[str, Any]:
    """
    Validate External API Connectivity And Response Times.
    
    Returns:
        Dict: External Service Health Status
    """
    try:
        import aiohttp
        
        # Test External APIs Used By AgriSenseGuardian
        TestEndpoints = [
            {'Name': 'Open-Meteo', 'URL': 'https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current=temperature_2m'},
            {'Name': 'NASA POWER', 'URL': 'https://power.larc.nasa.gov/api/temporal/daily/point?latitude=28.6139&longitude=77.2090&start=20241125&end=20241125&community=AG&parameters=T2M&format=JSON'},
            {'Name': 'ISRIC SoilGrids', 'URL': 'https://rest.isric.org/soilgrids/v2.0/classification/query?lat=28.6139&lon=77.2090'},
            {'Name': 'OpenStreetMap', 'URL': 'https://nominatim.openstreetmap.org/search?q=Delhi,India&format=json&limit=1'}
        ]
        
        ExternalResults = {}
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as Session:
            for Endpoint in TestEndpoints:
                try:
                    StartTime = time.time()
                    async with Session.get(Endpoint['URL'], headers={'User-Agent': 'AgriSenseGuardian-HealthCheck/1.0'}) as Response:
                        ResponseTime = (time.time() - StartTime) * 1000
                        ExternalResults[Endpoint['Name']] = {
                            'Status': 'Healthy' if Response.status == 200 else 'Degraded',
                            'StatusCode': Response.status,
                            'ResponseTime': round(ResponseTime, 2)
                        }
                except Exception as E:
                    ExternalResults[Endpoint['Name']] = {
                        'Status': 'Unhealthy',
                        'Error': str(E)
                    }
        
        HealthyCount = sum(1 for service in ExternalResults.values() if service['Status'] == 'Healthy')
        TotalCount = len(ExternalResults)
        
        return {
            'OverallStatus': 'Healthy' if HealthyCount >= TotalCount * 0.75 else 'Degraded',  # 75% threshold
            'HealthyServices': HealthyCount,
            'TotalServices': TotalCount,
            'Services': ExternalResults
        }
        
    except Exception as E:
        return {
            'OverallStatus': 'Error',
            'Error': str(E)
        }

async def RunComprehensiveHealthCheck() -> Dict[str, Any]:
    """
    Execute Complete System Health Assessment.
    
    Returns:
        Dict: Comprehensive Health Report With All Component Status
    """
    Logger.info("🏥 Starting AgriSenseGuardian Health Check...")
    
    StartTime = time.time()
    
    # Run All Health Checks Concurrently
    WebUIHealth, A2AHealth, ResourceHealth, ExternalHealth = await asyncio.gather(
        CheckWebUIHealth(),
        CheckA2AAgentsHealth(),
        CheckSystemResources(),
        CheckExternalDependencies()
    )
    
    TotalTime = round((time.time() - StartTime) * 1000, 2)
    
    # Determine Overall System Health
    HealthScores = []
    
    if WebUIHealth['Status'] == 'Healthy':
        HealthScores.append(1)
    else:
        HealthScores.append(0)
    
    if A2AHealth['OverallStatus'] == 'Healthy':
        HealthScores.append(1)
    elif A2AHealth['OverallStatus'] == 'Degraded':
        HealthScores.append(0.5)
    else:
        HealthScores.append(0)
    
    if ResourceHealth['Status'] == 'Healthy':
        HealthScores.append(1)
    elif ResourceHealth['Status'] == 'Warning':
        HealthScores.append(0.7)
    else:
        HealthScores.append(0)
    
    if ExternalHealth['OverallStatus'] == 'Healthy':
        HealthScores.append(1)
    elif ExternalHealth['OverallStatus'] == 'Degraded':
        HealthScores.append(0.5)
    else:
        HealthScores.append(0)
    
    OverallScore = sum(HealthScores) / len(HealthScores)
    
    if OverallScore >= 0.9:
        OverallStatus = 'Healthy'
    elif OverallScore >= 0.6:
        OverallStatus = 'Degraded'
    else:
        OverallStatus = 'Unhealthy'
    
    HealthReport = {
        'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'OverallStatus': OverallStatus,
        'OverallScore': round(OverallScore, 2),
        'CheckDuration': f"{TotalTime}ms",
        'Components': {
            'WebUI': WebUIHealth,
            'A2AAgents': A2AHealth,
            'SystemResources': ResourceHealth,
            'ExternalServices': ExternalHealth
        }
    }
    
    Logger.info(f"🏥 Health Check Complete: {OverallStatus} (Score: {OverallScore:.2f})")
    
    return HealthReport

def PrintHealthReport(HealthReport: Dict[str, Any]) -> None:
    """
    Pretty Print Health Check Results To Console.
    
    Args:
        HealthReport: Complete Health Assessment Results
    """
    print("\n" + "="*80)
    print("🌾 AGRISENSEGUARDIAN HEALTH CHECK REPORT")
    print("="*80)
    print(f"⏰ Timestamp: {HealthReport['Timestamp']}")
    print(f"🎯 Overall Status: {HealthReport['OverallStatus']}")
    print(f"📊 Health Score: {HealthReport['OverallScore']}/1.0")
    print(f"⚡ Check Duration: {HealthReport['CheckDuration']}")
    print("-"*80)
    
    # Web UI Component
    WebUI = HealthReport['Components']['WebUI']
    StatusIcon = "✅" if WebUI['Status'] == 'Healthy' else "❌"
    print(f"{StatusIcon} Web UI: {WebUI['Status']}")
    if 'ResponseTime' in WebUI:
        print(f"   └─ Response Time: {WebUI['ResponseTime']}ms")
    
    # A2A Agents Component
    A2A = HealthReport['Components']['A2AAgents']
    StatusIcon = "✅" if A2A['OverallStatus'] == 'Healthy' else ("⚠️" if A2A['OverallStatus'] == 'Degraded' else "❌")
    print(f"{StatusIcon} A2A Agents: {A2A['OverallStatus']} ({A2A['HealthyAgents']}/{A2A['TotalAgents']} Healthy)")
    
    # System Resources Component
    Resources = HealthReport['Components']['SystemResources']
    if Resources['Status'] != 'Unknown':
        StatusIcon = "✅" if Resources['Status'] == 'Healthy' else ("⚠️" if Resources['Status'] == 'Warning' else "❌")
        print(f"{StatusIcon} System Resources: {Resources['Status']}")
        print(f"   ├─ CPU: {Resources['CPU']['UsagePercent']}%")
        print(f"   ├─ Memory: {Resources['Memory']['UsagePercent']}% ({Resources['Memory']['Available']:.1f}GB Free)")
        print(f"   └─ Disk: {Resources['Disk']['UsagePercent']}% ({Resources['Disk']['Free']:.1f}GB Free)")
    
    # External Services Component
    External = HealthReport['Components']['ExternalServices']
    StatusIcon = "✅" if External['OverallStatus'] == 'Healthy' else ("⚠️" if External['OverallStatus'] == 'Degraded' else "❌")
    print(f"{StatusIcon} External Services: {External['OverallStatus']} ({External['HealthyServices']}/{External['TotalServices']} Healthy)")
    
    print("="*80)

def main():
    """
    Main Entry Point For Health Check Script.
    
    Supports Command Line Options For Different Output Formats.
    """
    import argparse
    
    Parser = argparse.ArgumentParser(description='AgriSenseGuardian Health Check')
    Parser.add_argument('--json', action='store_true', help='Output Results In JSON Format')
    Parser.add_argument('--quiet', '-q', action='store_true', help='Quiet Mode - Only Return Exit Code')
    Parser.add_argument('--timeout', '-t', type=int, default=30, help='Timeout In Seconds (Default: 30)')
    
    Args = Parser.parse_args()
    
    try:
        # Run Health Check With Timeout
        HealthReport = asyncio.wait_for(
            RunComprehensiveHealthCheck(),
            timeout=Args.timeout
        )
        HealthReport = asyncio.run(HealthReport)
        
        if Args.quiet:
            # Quiet Mode - Only Exit Code
            pass
        elif Args.json:
            # JSON Output Mode
            import json
            print(json.dumps(HealthReport, indent=2))
        else:
            # Default Pretty Print Mode
            PrintHealthReport(HealthReport)
        
        # Exit Code Based On Overall Health
        if HealthReport['OverallStatus'] == 'Healthy':
            sys.exit(0)
        elif HealthReport['OverallStatus'] == 'Degraded':
            sys.exit(1)
        else:
            sys.exit(2)
        
    except asyncio.TimeoutError:
        Logger.error(f"Health Check Timed Out After {Args.timeout} Seconds")
        sys.exit(3)
    except Exception as E:
        Logger.error(f"Health Check Failed: {str(E)}")
        sys.exit(4)

if __name__ == '__main__':
    main()