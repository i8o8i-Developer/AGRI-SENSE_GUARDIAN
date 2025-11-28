# ==============================================================================
# 🐳 AgriSenseGuardian Docker Container Configuration
# Multi-Stage Production-Ready Build For Agricultural AI Platform
# Optimized For Google Cloud Run And Kubernetes Deployment
# ==============================================================================

# ==============================
# 📦 Stage 1: Base Image Setup
# ==============================
FROM python:3.11-slim AS BaseStage

# 🏷️ Container Metadata Following Best Practices
LABEL maintainer="Anubhav Chaurasia <i8o8iworkstation@outlook.com>"
LABEL version="2.0.0"
LABEL description="AgriSenseGuardian - AI-Powered Agricultural Intelligence Platform"
LABEL project="Kaggle X Google Capstone Hackathon"
LABEL repository="https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN"

# 🛠️ Install System Dependencies Required For Agricultural Data Processing
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    libhdf5-dev \
    libnetcdf-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 👤 Create Non-Root User For Security Best Practices
RUN groupadd --gid 1000 agrisense \
    && useradd --uid 1000 --gid agrisense --shell /bin/bash --create-home agrisense

# 📂 Set Working Directory
WORKDIR /AgriSenseGuardian

# ==============================
# 📚 Stage 2: Dependencies
# ==============================
FROM BaseStage AS DependencyStage

# 📋 Copy Requirements First For Docker Layer Caching Optimization
COPY Requirements.txt pyproject.toml ./

# 🔧 Upgrade Pip And Install Python Dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r Requirements.txt

# ==============================
# 🚀 Stage 3: Application Build
# ==============================
FROM DependencyStage AS ApplicationStage

# 📁 Copy Application Source Code
COPY --chown=agrisense:agrisense . .

# 🔐 Set Proper File Permissions
RUN chmod -R 755 /AgriSenseGuardian \
    && chmod +x Main.py

# 📂 Create Required Directories For Logs And Temporary Data
RUN mkdir -p /AgriSenseGuardian/Logs \
    && mkdir -p /AgriSenseGuardian/Temp \
    && chown -R agrisense:agrisense /AgriSenseGuardian/Logs \
    && chown -R agrisense:agrisense /AgriSenseGuardian/Temp

# ==============================
# 🏃 Stage 4: Runtime Configuration
# ==============================
FROM ApplicationStage AS RuntimeStage

# 👤 Switch To Non-Root User
USER agrisense

# 🌐 Expose Application Port
EXPOSE 8000

# 📊 Expose Metrics Port For Prometheus Monitoring
EXPOSE 8001

# 🤖 Expose A2A Agent Communication Ports
EXPOSE 9000 9001 9002 9003

# 🔧 Environment Variables With Secure Defaults
ENV PYTHONPATH="/AgriSenseGuardian"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV API_HOST="0.0.0.0"
ENV API_PORT=8000
ENV A2A_HOST="0.0.0.0"
ENV START_A2A_ON_STARTUP=true
ENV LOG_LEVEL="INFO"

# ❤️ Health Check Configuration For Container Orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 🚀 Application Startup Command
CMD ["python", "Main.py"]

# ==============================================================================
# 📝 Container Usage Instructions:
#
# 🔨 Build Command:
#    docker build -t agrisense-guardian:latest .
#
# 🏃 Run Command (Development):
#    docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key agrisense-guardian:latest
#
# 🏃 Run Command (Production With Environment File):
#    docker run -p 8000:8000 --env-file .env agrisense-guardian:latest
#
# 📊 Run With All Ports Exposed:
#    docker run -p 8000:8000 -p 9000:9000 -p 9001:9001 -p 9002:9002 \
#               --env-file .env agrisense-guardian:latest
#
# 🔍 Container Shell Access (Debug):
#    docker exec -it container_name /bin/bash
#
# 📋 View Container Logs:
#    docker logs -f container_name
#
# ==============================================================================