from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Optional

# Prometheus
try:
    from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
    _PROM_AVAILABLE = True
except Exception:
    _PROM_AVAILABLE = False

# OpenTelemetry (Optional)
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    _OTEL_AVAILABLE = True
except Exception:
    _OTEL_AVAILABLE = False


# ===== Prometheus Metrics =====
REGISTRY: Optional[CollectorRegistry] = None

if _PROM_AVAILABLE:
    REGISTRY = CollectorRegistry()
    AGENT_DURATION = Histogram(
        "agent_execution_seconds",
        "Agent Execution Duration In Seconds",
        ["agent"],
        registry=REGISTRY
    )
    AGENT_DURATION_LABELED = Histogram(
        "agent_execution_seconds_labeled",
        "Agent Execution Duration In Seconds With Labels",
        ["agent", "location", "iteration"],
        registry=REGISTRY
    )
    TOOL_CALLS = Counter(
        "tool_calls_total",
        "Total Tool Invocations",
        ["tool"],
        registry=REGISTRY
    )
    ERRORS = Counter(
        "agent_errors_total",
        "Total Agent Errors",
        ["agent"],
        registry=REGISTRY
    )
else:
    AGENT_DURATION = AGENT_DURATION_LABELED = TOOL_CALLS = ERRORS = None


def metrics_response():
    """
    Generate Prometheus Metrics Response For HTTP Endpoint.
    
    Returns Current Metrics In Prometheus Exposition Format For Scraping
    By Monitoring Systems. Includes Agent Execution Times, Tool Call Counts,
    And Error Rates For System Observability.
    
    Returns:
        Tuple[bytes, str]: (Metrics Data, Content Type) For HTTP Response
    """
    if _PROM_AVAILABLE and REGISTRY is not None:
        return generate_latest(REGISTRY), CONTENT_TYPE_LATEST
    return b"", "text/plain"


# ===== OpenTelemetry Tracing =====
_TRACER = None


def setup_tracing(service_name: str = "AgriSenseGuardian"):
    """
    Initialize OpenTelemetry Tracing Infrastructure.
    
    Sets Up Distributed Tracing With OTLP Export For Request Flow Analysis
    And Performance Monitoring Across Multi-Agent Interactions.
    
    Args:
        service_name: Service Identifier For Trace Attribution
        
    Returns:
        TracerProvider: Configured Tracer Provider (None If OTEL Unavailable)
    """
    """Disabled - OpenTelemetry Tracing Not Configured"""
    return None


@contextmanager
def use_span(name: str):
    """
    Create A Tracing Span Context For Operation Tracking.
    
    Context Manager That Creates A Trace Span For The Specified Operation,
    Enabling Distributed Tracing Of Agent Interactions And Tool Calls.
    
    Args:
        name: Descriptive Name For The Operation Being Traced
    """
    """No-Op Span Context For When Tracing Is Disabled"""
    yield None


@contextmanager
def record_agent_duration(agent_name: str):
    """
    Record Execution Duration For Agent Operations.
    
    Context Manager That Measures And Records The Execution Time Of Agent
    Operations Using Prometheus Histograms For Performance Monitoring.
    
    Args:
        agent_name: Name Of The Agent Being Measured
    """
    start = time.time()
    try:
        yield
    finally:
        if _PROM_AVAILABLE and AGENT_DURATION is not None:
            AGENT_DURATION.labels(agent=agent_name).observe(time.time() - start)


@contextmanager
def record_agent_duration_ex(agent_name: str, location: str | None = None, iteration: int | None = None):
    """
    Record Detailed Agent Execution Metrics With Labels.
    
    Extended Version Of Duration Recording That Includes Location And Iteration
    Context For More Granular Performance Analysis And Debugging.
    
    Args:
        agent_name: Name Of The Agent Being Measured
        location: Geographic Location Context (Optional)
        iteration: Workflow Iteration Number (Optional)
    """
    start = time.time()
    try:
        yield
    finally:
        if _PROM_AVAILABLE and AGENT_DURATION_LABELED is not None:
            labels = {"agent": agent_name}
            if location:
                labels["location"] = location
            if iteration is not None:
                labels["iteration"] = str(iteration)
            AGENT_DURATION_LABELED.labels(**labels).observe(time.time() - start)


def inc_tool(tool_name: str):
    """
    Increment Tool Usage Counter For Observability.
    
    Records Tool Invocation Events For Usage Pattern Analysis And
    Integration Monitoring Across The Multi-Agent System.
    
    Args:
        tool_name: Name Of The Tool That Was Called
    """
    if _PROM_AVAILABLE and TOOL_CALLS is not None:
        TOOL_CALLS.labels(tool=tool_name).inc()


def inc_error(agent_name: str):
    """
    Increment Error Counter For Agent Reliability Tracking.
    
    Records Error Events By Agent For Failure Rate Analysis And
    System Health Monitoring.
    
    Args:
        agent_name: Name Of The Agent Where Error Occurred
    """
    if _PROM_AVAILABLE and ERRORS is not None:
        ERRORS.labels(agent=agent_name).inc()


__all__ = [
    "setup_tracing", "use_span", "record_agent_duration",
    "inc_tool", "inc_error", "metrics_response"
]