# Centralized Configuration Management For AgriSenseGuardian
# Implements Pydantic BaseSettings For Type-Safe, Environment-Driven Configuration
# Provides Sensible Defaults For Local Development While Supporting Production Overrides

import os
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class A2APorts(BaseSettings):
    """
    Configuration For Agent-to-Agent (A2A) Communication Ports.
    
    Defines The Network Ports Used By Individual Agent Servers In The
    Multi-Agent Architecture. Each Agent Runs As A Separate Process
    And Communicates Via HTTP APIs On Designated Ports.
    """
    orchestrator_port: int = Field(default=9000, description="Port For Orchestrator Agent Server")
    forecast_port: int = Field(default=9001, description="Port For Forecast Agent Server")
    verify_port: int = Field(default=9002, description="Port For Verify Agent Server")

    # Maintain Backward Compatibility With Existing Code That Uses Property Access
    @property
    def orchestrator(self) -> int:
        return self.orchestrator_port

    @property
    def forecast(self) -> int:
        return self.forecast_port

    @property
    def verify(self) -> int:
        return self.verify_port


class Settings(BaseSettings):
    """
    Main Configuration Class For AgriSenseGuardian Application.
    
    Centralizes All Application Settings Including API Keys, Network Configuration,
    Feature Flags, And External Service Credentials. Uses Pydantic For Type Safety
    And Environment Variable Loading With Sensible Defaults For Development.
    
    Email Configuration For Notifications. A2A Ports Are Managed Through The
    Nested A2APorts Configuration Class.
    """
    # API Keys / External Services
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    openweather_api_key: Optional[str] = Field(default=None, env="OPENWEATHER_API_KEY")
    copernicus_api_key: Optional[str] = Field(default=None, env="COPERNICUS_API_KEY")
    sentinel_client_id: Optional[str] = Field(default=None, env="SENTINEL_CLIENT_ID")
    sentinel_client_secret: Optional[str] = Field(default=None, env="SENTINEL_CLIENT_SECRET")

    # Web API Host
    api_host: str = Field(default="127.0.0.1", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")

    # Logging
    log_level: str = Field(default="INFO")

    # Feature Flags
    evaluation_mode: bool = Field(default=False)

    # A2A
    a2a_host: str = Field(default="0.0.0.0", env="A2A_HOST")
    a2a_ports: A2APorts = Field(default_factory=A2APorts)
    start_a2a_on_startup: bool = Field(default=True, env="START_A2A_ON_STARTUP")

    # Note: SMS Settings Are Deprecated. Email Is The Primary Notification Channel.

    # Email (SMTP)
    smtp_provider: Optional[str] = Field(default=None, env="SMTP_PROVIDER")
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_port: Optional[int] = Field(default=587, env="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, env="SMTP_USER")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    sender_email: Optional[str] = Field(default=None, env="SENDER_EMAIL")
    sender_name: Optional[str] = Field(default="AgriSenseGuardian", env="SENDER_NAME")

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Retrieve The Singleton Settings Instance.
    
    Creates And Returns A Cached Instance Of The Settings Class, Loading
    Configuration From Environment Variables And .env File. The LRU Cache
    Ensures That Settings Are Only Loaded Once Per Application Lifecycle
    For Optimal Performance.
    
    Returns:
        Settings: The Configured Application Settings Instance.
    """
    return Settings()