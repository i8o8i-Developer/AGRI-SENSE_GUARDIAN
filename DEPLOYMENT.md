# 🐳 AgriSenseGuardian Docker Deployment Guide

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    DOCKER DEPLOYMENT DOCUMENTATION                        ║
║              Production-Ready Container Deployment Guide                  ║
║                         AgriSenseGuardian Platform                        ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 Overview

This Guide Provides Comprehensive Instructions For Deploying AgriSenseGuardian Using Docker Containers. The Platform Is Containerized Using Multi-Stage Docker Builds For Optimal Performance, Security, And Scalability In Production Environments.

### **Container Architecture**
- **Base Image**: Python 3.11 Slim (Debian-Based)
- **Multi-Stage Build**: Optimized For Layer Caching And Reduced Image Size
- **Non-Root User**: Security-First Approach With Dedicated `agrisense` User
- **Health Checks**: Built-In Container Health Monitoring
- **Port Exposure**: Web UI (8000) + A2A Agents (9000-9003) + Metrics (8001)

---

## 🚀 Quick Start Deployment

### **Prerequisites**
- Docker Engine 20.10+ Or Docker Desktop
- 4GB RAM Minimum (8GB Recommended)
- 2 CPU Cores (4 Recommended)
- Internet Connection For Data APIs

### **1. Build Container Image**

```bash
# Clone Repository (If Not Already Done)
git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git
cd AGRI-SENSE_GUARDIAN

# Build Docker Image
docker build -t agrisense-guardian:latest .
```

### **2. Environment Configuration**

**Step-by-Step Environment Setup:**

1. **Copy Environment Template**
   ```bash
   cp .env.example .env
   ```

2. **Edit The `.env` File With Your Actual API Keys:**
   Replace the placeholder values in `.env` with your real credentials:

```env
# ══════════════════════════════════════════════════════════════════════════════
# 🔑 CORE API CREDENTIALS (REQUIRED)
# ══════════════════════════════════════════════════════════════════════════════

# Google Gemini AI (Required For Multi-Agent System)
GOOGLE_API_KEY=Your_Google_Api_Key_Here

# ══════════════════════════════════════════════════════════════════════════════
# 🌦️ WEATHER & CLIMATE DATA APIs (ENHANCED FORECASTING)
# ══════════════════════════════════════════════════════════════════════════════

# OpenWeatherMap API (Optional - Enhanced Geocoding & Weather Fallback)
# Free Tier: 1,000 Calls/Day | Sign Up: https://openweathermap.org/api
OPENWEATHER_API_KEY=Your_Openweather_Key_Here

# NASA POWER API (FREE - No Key Required)
# Provides: Satellite Data, Solar Radiation, Agricultural Parameters
# Used By: SatelliteTool, SoilTestTool (Automatic Fallback)
# Website: https://power.larc.nasa.gov/

# Open-Meteo API (FREE - No Key Required)
# Provides: Global Weather Forecasts, Historical Data
# Used By: WeatherTool (Primary Weather Source)
# Website: https://open-meteo.com/

# ══════════════════════════════════════════════════════════════════════════════
# 🛰️ SATELLITE & SOIL DATA APIs (PRECISION AGRICULTURE)
# ══════════════════════════════════════════════════════════════════════════════

# Copernicus Climate Data Store (Optional - Professional Satellite Analytics)
# Format: uid:api_key | Free Registration Required
# Provides: ERA5-Land Data, Soil Moisture, Evapotranspiration, NDVI
# Sign Up: https://cds.climate.copernicus.eu/api-how-to
COPERNICUS_API_KEY=Your_Copernicus_Uid:Api_Key

# ISRIC SoilGrids API (FREE - No Key Required)
# Provides: Global Soil Property Data, Soil Classification
# Used By: SoilTestTool (Regional Fallback)
# Website: https://soilgrids.org/

# USGS Soil Data Access (FREE - No Key Required)
# Provides: US Soil Survey Data, Soil Properties
# Used By: SoilTestTool (US Region Fallback)
# Website: https://sdmdataaccess.nrcs.usda.gov/

# FAO HWSD (FREE - Dataset Download Required)
# Provides: Harmonized World Soil Database
# Used By: SoilTestTool (Global Soil Classification)
# Website: https://www.fao.org/soils-portal/data-hub/

# ══════════════════════════════════════════════════════════════════════════════
# 🔍 SEARCH & INFORMATION RETRIEVAL APIs (INTELLIGENT WEB SEARCH)
# ══════════════════════════════════════════════════════════════════════════════

# Google Custom Search Engine (Optional - Agricultural Content Search)
# Requires: Both GOOGLE_API_KEY + GOOGLE_SEARCH_ENGINE_ID
# Setup Guide: https://developers.google.com/custom-search/v1/overview
GOOGLE_SEARCH_ENGINE_ID=Your_Search_Engine_Id_Here

# SerpAPI (Optional - Enhanced Search Results)
# Free Tier: 100 Searches/Month | Sign Up: https://serpapi.com/
SERPAPI_API_KEY=Your_SerpApi_Key_Here

# OpenStreetMap Nominatim (FREE - No Key Required)
# Provides: Global Geocoding Services, Location Resolution
# Used By: All Tools For Address → Coordinates Conversion
# Website: https://nominatim.openstreetmap.org/

# ══════════════════════════════════════════════════════════════════════════════
# 📧 EMAIL NOTIFICATION SYSTEM (FARMER COMMUNICATIONS)
# ══════════════════════════════════════════════════════════════════════════════

# SMTP Configuration (Email Delivery)
SMTP_PROVIDER=gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=Your_Email@gmail.com
SMTP_PASSWORD=Your_App_Password
SENDER_EMAIL=Your_Email@gmail.com
SENDER_NAME=AgriSenseGuardian

# Alternative SMTP Providers:
# ─────────────────────────────
# Outlook: smtp.office365.com:587
# Yahoo: smtp.mail.yahoo.com:587
# SendGrid: smtp.sendgrid.net:587
# Mailgun: smtp.mailgun.org:587

# ══════════════════════════════════════════════════════════════════════════════
# 🔧 APPLICATION CONFIGURATION (SERVER SETTINGS)
# ══════════════════════════════════════════════════════════════════════════════

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
START_A2A_ON_STARTUP=true
LOG_LEVEL=INFO

# Session & Memory Configuration
SESSION_PROVIDER=InMemorySessionService
MAX_SESSION_HISTORY=100
SESSION_TIMEOUT_MINUTES=30

# Observability & Monitoring
ENABLE_METRICS=true
METRICS_PORT=8001
ENABLE_TRACING=true
HEALTH_CHECK_INTERVAL=30

# Rate Limiting & Security
MAX_REQUESTS_PER_MINUTE=60
API_KEY_REQUIRED=false
CORS_ORIGINS=*
```

**⚠️ Important Environment Notes:**
- **Never Commit `.env`** - The `.env` file contains sensitive API keys and should never be committed to version control
- **Use `.env.example` as Template** - The `.env.example` file shows all available configuration options with placeholder values
- **Cloud Deployments** - All cloud deployment commands reference your local `.env` file or use environment variable substitution
- **Docker Integration** - The Dockerfile and docker-compose configurations are designed to work with your `.env` file automatically
- **Local Development** - The application automatically loads environment variables from `.env` using python-dotenv

### **3. Run Container**

#### **Development Mode (Single Port)**
```bash
docker run -d \
  --name agrisense-dev \
  -p 8000:8000 \
  --env-file .env \
  agrisense-guardian:latest
```

#### **Production Mode (All Ports)**
```bash
docker run -d \
  --name agrisense-production \
  -p 8000:8000 \
  -p 9000:9000 \
  -p 9001:9001 \
  -p 9002:9002 \
  -p 8001:8001 \
  --env-file .env \
  --restart unless-stopped \
  agrisense-guardian:latest
```

### **4. Verify Deployment**

```bash
# Check Container Status
docker ps

# View Application Logs
docker logs -f agrisense-production

# Test Health Endpoint
curl http://localhost:8000/health

# Test Readiness Endpoint
curl http://localhost:8000/readiness

# Access Web UI
open http://localhost:8000
```

---

## 🌐 Cloud Deployment Options

### **📋 General Prerequisites (All Cloud Platforms)**

**Source Code Acquisition:**
- **GitHub Repository**: https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN
- **Method 1**: Clone repository locally → Build → Push to cloud
- **Method 2**: Direct build from GitHub (Cloud Build integration)
- **Method 3**: Fork repository → Deploy from your fork

**Required Files:**
- `Dockerfile` (Multi-stage production build) ✅ Included
- `.dockerignore` (Build optimization) ✅ Included  
- `Requirements.txt` (Python dependencies) ✅ Included
- `.env.example` (Environment template) ✅ Included

**Build Process:**
1. **Clone** → `git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git`
2. **Configure** → Copy `.env.example` to `.env` and add your API keys
3. **Build** → `docker build -t agrisense-guardian .`
4. **Deploy** → Push to cloud container registry and deploy

---

### **Google Cloud Run (Recommended)**

#### **Prerequisites & Source Setup**
```bash
# 1. Clone The Repository (Source Code)
git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git
cd AGRI-SENSE_GUARDIAN

# 2. Set Up Google Cloud Project
gcloud config set project YOUR_PROJECT_ID
gcloud auth login
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 3. Create .env File With Your API Keys
cp .env.example .env
# Edit .env file and replace placeholder values with your actual API keys:
# - GOOGLE_API_KEY=your_actual_google_api_key
# - OPENWEATHER_API_KEY=your_actual_openweather_key
# - COPERNICUS_API_KEY=your_uid:your_api_key
# - SMTP_USER=your_email@gmail.com
# - SMTP_PASSWORD=your_app_password
# (See .env.example for complete list of configurable variables)
```

#### **Deploy To Cloud Run**
```bash
# Direct Build From Source (Recommended)
# This builds from your local source code directory
gcloud builds submit --tag gcr.io/PROJECT_ID/agrisense-guardian .

# Deploy To Cloud Run
gcloud run deploy agrisense-guardian \
  --image gcr.io/PROJECT_ID/agrisense-guardian \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=Your_Api_Key \
  --port 8000 \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

#### **Environment Variables Setup**

**Method 1: Deploy With Environment File (Recommended)**
```bash
# Deploy Cloud Run With Environment Variables From .env File
# Note: Ensure your .env file is configured locally first
gcloud run deploy agrisense-guardian \
  --image gcr.io/PROJECT_ID/agrisense-guardian \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --env-vars-file .env \
  --port 8000 \
  --memory 6Gi \
  --cpu 2 \
  --max-instances 10
```

**Method 2: Manual Environment Variables Setup**
```bash
# Set Core Environment Variables (Use Your Actual Values From .env File)
gcloud run services update agrisense-guardian \
  --set-env-vars GOOGLE_API_KEY="$(grep GOOGLE_API_KEY .env | cut -d '=' -f2)",START_A2A_ON_STARTUP=true,LOG_LEVEL=INFO \
  --region us-central1

# Set Optional Environment Variables (If Configured In .env)
gcloud run services update agrisense-guardian \
  --set-env-vars OPENWEATHER_API_KEY="$(grep OPENWEATHER_API_KEY .env | cut -d '=' -f2)",COPERNICUS_API_KEY="$(grep COPERNICUS_API_KEY .env | cut -d '=' -f2)",GOOGLE_SEARCH_ENGINE_ID="$(grep GOOGLE_SEARCH_ENGINE_ID .env | cut -d '=' -f2)",SERPAPI_API_KEY="$(grep SERPAPI_API_KEY .env | cut -d '=' -f2)" \
  --region us-central1

# Set Email Configuration (If Email Notifications Required)
gcloud run services update agrisense-guardian \
  --set-env-vars SMTP_HOST=smtp.gmail.com,SMTP_PORT=587,SMTP_USER="$(grep SMTP_USER .env | cut -d '=' -f2)",SMTP_PASSWORD="$(grep SMTP_PASSWORD .env | cut -d '=' -f2)",SENDER_EMAIL="$(grep SENDER_EMAIL .env | cut -d '=' -f2)",SENDER_NAME=AgriSenseGuardian \
  --region us-central1
```

### **AWS Fargate**

#### **Prerequisites & Source Setup**
```bash
# 1. Clone The Repository (Source Code)
git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git
cd AGRI-SENSE_GUARDIAN

# 2. Set Up AWS CLI
aws configure
# Enter your AWS Access Key ID, Secret Access Key, Region

# 3. Create ECR Repository For Container Images
aws ecr create-repository --repository-name agrisense-guardian --region us-east-1

# 4. Build And Push Docker Image To ECR
# Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image from source
docker build -t agrisense-guardian .

# Tag and push to ECR
docker tag agrisense-guardian:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agrisense-guardian:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agrisense-guardian:latest
```

#### **Task Definition**
```json
{
  "family": "agrisense-guardian",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "agrisense-guardian",
      "image": "your-account.dkr.ecr.region.amazonaws.com/agrisense-guardian:latest",
      "portMappings": [
        {"containerPort": 8000, "protocol": "tcp"}
      ],
      "environment": [
        {"name": "GOOGLE_API_KEY", "value": "${GOOGLE_API_KEY}"},
        {"name": "START_A2A_ON_STARTUP", "value": "true"},
        {"name": "LOG_LEVEL", "value": "INFO"},
        {"name": "OPENWEATHER_API_KEY", "value": "${OPENWEATHER_API_KEY}"},
        {"name": "COPERNICUS_API_KEY", "value": "${COPERNICUS_API_KEY}"},
        {"name": "GOOGLE_SEARCH_ENGINE_ID", "value": "${GOOGLE_SEARCH_ENGINE_ID}"},
        {"name": "SERPAPI_API_KEY", "value": "${SERPAPI_API_KEY}"},
        {"name": "SMTP_HOST", "value": "smtp.gmail.com"},
        {"name": "SMTP_PORT", "value": "587"},
        {"name": "SMTP_USER", "value": "${SMTP_USER}"},
        {"name": "SMTP_PASSWORD", "value": "${SMTP_PASSWORD}"},
        {"name": "SENDER_EMAIL", "value": "${SENDER_EMAIL}"},
        {"name": "SENDER_NAME", "value": "AgriSenseGuardian"}
      ],
      "secrets": [
        {"name": "GOOGLE_API_KEY", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/google-api-key"},
        {"name": "OPENWEATHER_API_KEY", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/openweather-api-key"},
        {"name": "COPERNICUS_API_KEY", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/copernicus-api-key"},
        {"name": "GOOGLE_SEARCH_ENGINE_ID", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/google-search-id"},
        {"name": "SERPAPI_API_KEY", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/serpapi-key"},
        {"name": "SMTP_USER", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/smtp-user"},
        {"name": "SMTP_PASSWORD", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/smtp-password"},
        {"name": "SENDER_EMAIL", "valueFrom": "arn:aws:ssm:region:account:parameter/agrisense/sender-email"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/agrisense-guardian",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**AWS Parameter Store Setup (Required For Secret Management):**
```bash
# Store API Keys Securely In AWS Systems Manager Parameter Store
# Run These Commands With Your .env File Configured Locally

aws ssm put-parameter \
  --name "/agrisense/google-api-key" \
  --value "$(grep GOOGLE_API_KEY .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "Google Gemini API Key for AgriSense Guardian"

aws ssm put-parameter \
  --name "/agrisense/openweather-api-key" \
  --value "$(grep OPENWEATHER_API_KEY .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "OpenWeatherMap API Key"

aws ssm put-parameter \
  --name "/agrisense/copernicus-api-key" \
  --value "$(grep COPERNICUS_API_KEY .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "Copernicus Climate Data Store API Key"

aws ssm put-parameter \
  --name "/agrisense/google-search-id" \
  --value "$(grep GOOGLE_SEARCH_ENGINE_ID .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "Google Custom Search Engine ID"

aws ssm put-parameter \
  --name "/agrisense/serpapi-key" \
  --value "$(grep SERPAPI_API_KEY .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "SerpAPI Key for Enhanced Search"

aws ssm put-parameter \
  --name "/agrisense/smtp-user" \
  --value "$(grep SMTP_USER .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "SMTP Username for Email Notifications"

aws ssm put-parameter \
  --name "/agrisense/smtp-password" \
  --value "$(grep SMTP_PASSWORD .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "SMTP Password for Email Notifications"

aws ssm put-parameter \
  --name "/agrisense/sender-email" \
  --value "$(grep SENDER_EMAIL .env | cut -d '=' -f2)" \
  --type "SecureString" \
  --description "Sender Email Address"
```

**Note:** Replace `region` and `account` with your actual AWS region and account ID in the task definition ARNs above.

### **Azure Container Instances**

#### **Prerequisites & Source Setup**
```bash
# 1. Clone The Repository (Source Code)
git clone https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN.git
cd AGRI-SENSE_GUARDIAN

# 2. Set Up Azure CLI
az login
az account set --subscription YOUR_SUBSCRIPTION_ID

# 3. Create Resource Group
az group create --name agrisense-rg --location eastus

# 4. Create Azure Container Registry (ACR)
az acr create --resource-group agrisense-rg --name agrisenseregistry --sku Basic --admin-enabled true

# 5. Build And Push Image To ACR
# Login to ACR
az acr login --name agrisenseregistry

# Build and push from source
az acr build --registry agrisenseregistry --image agrisense-guardian:latest .

# Or build locally and push
# docker build -t agrisense-guardian .
# docker tag agrisense-guardian agrisenseregistry.azurecr.io/agrisense-guardian:latest
# docker push agrisenseregistry.azurecr.io/agrisense-guardian:latest
```

#### **Deploy To Azure Container Instances**
```bash
az container create \
  --resource-group agrisense-rg \
  --name agrisense-guardian \
  --image agrisenseregistry.azurecr.io/agrisense-guardian:latest \
  --dns-name-label agrisense-guardian \
  --ports 8000 \
  --environment-variables \
    GOOGLE_API_KEY="$(grep GOOGLE_API_KEY .env | cut -d '=' -f2)" \
    START_A2A_ON_STARTUP=true \
    LOG_LEVEL=INFO \
    OPENWEATHER_API_KEY="$(grep OPENWEATHER_API_KEY .env | cut -d '=' -f2)" \
    COPERNICUS_API_KEY="$(grep COPERNICUS_API_KEY .env | cut -d '=' -f2)" \
    GOOGLE_SEARCH_ENGINE_ID="$(grep GOOGLE_SEARCH_ENGINE_ID .env | cut -d '=' -f2)" \
    SERPAPI_API_KEY="$(grep SERPAPI_API_KEY .env | cut -d '=' -f2)" \
    SMTP_HOST=smtp.gmail.com \
    SMTP_PORT=587 \
    SMTP_USER="$(grep SMTP_USER .env | cut -d '=' -f2)" \
    SMTP_PASSWORD="$(grep SMTP_PASSWORD .env | cut -d '=' -f2)" \
    SENDER_EMAIL="$(grep SENDER_EMAIL .env | cut -d '=' -f2)" \
    SENDER_NAME=AgriSenseGuardian \
  --cpu 2 \
  --memory 4
```

---

## 📊 Container Monitoring

### **Health Check Endpoints**
- **Basic Health**: `GET /health`
- **Detailed Readiness**: `GET /readiness`
- **Agent Status**: `GET /agents/status`
- **Prometheus Metrics**: `GET /metrics`

### **Docker Health Status**
```bash
# Check Container Health
docker inspect --format='{{.State.Health.Status}}' agrisense-production

# View Health Check History
docker inspect --format='{{range .State.Health.Log}}{{.Start}} - {{.Output}}{{end}}' agrisense-production
```

### **Log Management**
```bash
# Follow Live Logs
docker logs -f agrisense-production

# Export Logs To File
docker logs agrisense-production > /path/to/agrisense.log 2>&1

# View Last 100 Lines
docker logs --tail 100 agrisense-production
```

---

## 🔧 Advanced Configuration

### **Resource Limits**
```bash
# Run With Resource Constraints
docker run -d \
  --name agrisense-production \
  --memory=4g \
  --cpus="2.0" \
  --memory-swap=6g \
  -p 8000:8000 \
  --env-file .env \
  agrisense-guardian:latest
```

### **Volume Mounts For Persistence**
```bash
# Create Persistent Volumes For Logs And Data
docker volume create agrisense-logs
docker volume create agrisense-data

# Run With Mounted Volumes
docker run -d \
  --name agrisense-production \
  -p 8000:8000 \
  -v agrisense-logs:/AgriSenseGuardian/Logs \
  -v agrisense-data:/AgriSenseGuardian/Data \
  --env-file .env \
  agrisense-guardian:latest
```

### **Network Configuration**
```bash
# Create Custom Network
docker network create agrisense-network

# Run Container In Custom Network
docker run -d \
  --name agrisense-production \
  --network agrisense-network \
  -p 8000:8000 \
  --env-file .env \
  agrisense-guardian:latest
```

---

## 🛠️ Development Workflow

### **Development Container**
```bash
# Run In Development Mode With Code Mounting
docker run -it \
  --name agrisense-dev \
  -p 8000:8000 \
  -v $(pwd):/AgriSenseGuardian \
  --env-file .env \
  agrisense-guardian:latest bash
```

### **Debugging**
```bash
# Access Running Container Shell
docker exec -it agrisense-production /bin/bash

# Run Python Commands Inside Container
docker exec -it agrisense-production python -c "import sys; print(sys.version)"

# Check Environment Variables
docker exec -it agrisense-production env | grep GOOGLE
```

### **Container Registry Management**
```bash
# Tag For Different Environments
docker tag agrisense-guardian:latest agrisense-guardian:production
docker tag agrisense-guardian:latest agrisense-guardian:staging

# Push To Registry
docker push your-registry.com/agrisense-guardian:latest
```

---

## 🚨 Production Considerations

### **Security Best Practices**
- ✅ Non-Root User Execution
- ✅ Minimal Base Image (Python 3.11 Slim)
- ✅ No API Keys In Image Layers
- ✅ Health Check Implementation
- ✅ Resource Limits Configuration

### **Scaling Recommendations**
- **CPU**: 2-4 Cores For Multi-Agent Processing
- **Memory**: 4-8GB For Satellite Data Processing
- **Storage**: 10GB For Logs And Temporary Data
- **Network**: High Bandwidth For API Calls

### **Monitoring Integration**
```bash
# Run With Prometheus Metrics Exposed
docker run -d \
  --name agrisense-production \
  -p 8000:8000 \
  -p 8001:8001 \
  --env-file .env \
  --label prometheus.scrape=true \
  --label prometheus.port=8001 \
  agrisense-guardian:latest
```

---

## 📊 API Reference & Data Sources

### **Core APIs (Required)**

#### **Google Gemini 2.5 Flash Lite**
- **Purpose**: Multi-Agent AI Processing Engine
- **Usage**: Powers All 4 Agents (Orchestrator, Forecast, Verify, Planner)
- **Cost**: Free Tier Available
- **Setup**: Get API Key From [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Environment**: `GOOGLE_API_KEY=Your_Google_Api_Key_Here`

### **Weather & Climate APIs (FREE)**

#### **Open-Meteo API**
- **Purpose**: Primary Weather Data Source (No Key Required)
- **Coverage**: Global Weather Forecasts, Historical Data
- **Used By**: WeatherTool (Primary Source)
- **Features**: Temperature, Precipitation, Wind, Humidity
- **Website**: [open-meteo.com](https://open-meteo.com/)

#### **NASA POWER API**
- **Purpose**: Satellite Agricultural Data (No Key Required)
- **Coverage**: Global Agricultural Climate Data (40+ Years)
- **Used By**: SatelliteTool, SoilTestTool
- **Features**: Solar Radiation, Evapotranspiration, Soil Moisture
- **Website**: [power.larc.nasa.gov](https://power.larc.nasa.gov/)

#### **OpenWeatherMap API**
- **Purpose**: Enhanced Weather & Geocoding (Optional)
- **Coverage**: Global Weather + Geocoding Services
- **Free Tier**: 1,000 Calls/Day
- **Used By**: WeatherTool (Fallback), All Tools (Geocoding)
- **Setup**: [openweathermap.org/api](https://openweathermap.org/api)
- **Environment**: `OPENWEATHER_API_KEY=Your_Openweather_Key_Here`

### **Satellite & Soil Data APIs**

#### **Copernicus Climate Data Store**
- **Purpose**: Professional Satellite Analytics (Optional)
- **Coverage**: European Space Agency Satellite Data
- **Used By**: CopernicusTool
- **Features**: ERA5-Land, Soil Moisture, NDVI, Evapotranspiration
- **Setup**: [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu/api-how-to)
- **Environment**: `COPERNICUS_API_KEY=Uid:Api_Key`

#### **ISRIC SoilGrids API**
- **Purpose**: Global Soil Property Data (No Key Required)
- **Coverage**: Worldwide Soil Classification & Properties
- **Used By**: SoilTestTool (Regional Fallback)
- **Features**: pH, Organic Carbon, Texture, Bulk Density
- **Website**: [soilgrids.org](https://soilgrids.org/)

#### **USGS Soil Data Access**
- **Purpose**: US Soil Survey Data (No Key Required)
- **Coverage**: United States Soil Properties
- **Used By**: SoilTestTool (US Region)
- **Features**: Field-Measured Soil Properties, Survey Data
- **Website**: [sdmdataaccess.nrcs.usda.gov](https://sdmdataaccess.nrcs.usda.gov/)

### **Search & Information APIs**

#### **Google Custom Search Engine**
- **Purpose**: Agricultural Content Search (Optional)
- **Coverage**: Targeted Agricultural Information Search
- **Used By**: GoogleSearchTool (Primary Search)
- **Setup**: Requires Both `GOOGLE_API_KEY` + `GOOGLE_SEARCH_ENGINE_ID`
- **Guide**: [developers.google.com/custom-search](https://developers.google.com/custom-search/v1/overview)

#### **SerpAPI**
- **Purpose**: Enhanced Web Search Results (Optional)
- **Coverage**: Comprehensive Search Results
- **Free Tier**: 100 Searches/Month
- **Used By**: GoogleSearchTool (Fallback Search)
- **Setup**: [serpapi.com](https://serpapi.com/)
- **Environment**: `SERPAPI_API_KEY=your_key`

#### **OpenStreetMap Nominatim**
- **Purpose**: Global Geocoding Services (No Key Required)
- **Coverage**: Worldwide Address → Coordinates Conversion
- **Used By**: All Tools (Location Resolution)
- **Features**: Free Geocoding, No Rate Limits For Reasonable Use
- **Website**: [nominatim.openstreetmap.org](https://nominatim.openstreetmap.org/)

### **Email & Communication APIs**

#### **SMTP Providers (Email Notifications)**
- **Purpose**: Farmer Communication & Action Plan Delivery
- **Used By**: EmailNotificationTool
- **Supported Providers**:
  - **Gmail**: `smtp.gmail.com:587` (App Password Required)
  - **Outlook**: `smtp.office365.com:587`
  - **Yahoo**: `smtp.mail.yahoo.com:587`
  - **SendGrid**: `smtp.sendgrid.net:587`
  - **Mailgun**: `smtp.mailgun.org:587`

### **API Usage Statistics & Limits**

| API Service | Free Tier | Rate Limit | Used By |
|-------------|-----------|------------|---------|
| Google Gemini | 15 RPM | 15 Requests/Minute | All Agents |
| Open-Meteo | Unlimited | No Limit | WeatherTool |
| NASA POWER | Unlimited | No Limit | SatelliteTool, SoilTestTool |
| OpenWeatherMap | 1,000/Day | 60 Calls/Minute | WeatherTool (Fallback) |
| Copernicus CDS | Unlimited | Download Limits | CopernicusTool |
| Google CSE | 100/Day | 10 Queries/Second | GoogleSearchTool |
| SerpAPI | 100/Month | No Limit | GoogleSearchTool (Fallback) |
| Nominatim | Unlimited | 1 Request/Second | All Tools (Geocoding) |

### **Fallback Strategy**

AgriSenseGuardian Implements Intelligent API Fallbacks:

1. **Weather Data**: Open-Meteo (Primary) → NASA POWER (Fallback) → OpenWeatherMap (Enhanced)
2. **Soil Data**: NASA POWER (Primary) → Regional Database (Fallback)
3. **Search**: Google CSE (Primary) → SerpAPI (Fallback)
4. **Geocoding**: Nominatim (Primary) → OpenWeatherMap (Enhanced)

**🎯 Recommendation**: Only `GOOGLE_API_KEY` Is Required. All Other APIs Are Optional Enhancements.

---

## 🔗 Integration Examples

### **Load Balancer Configuration (Nginx)**
```nginx
upstream agrisense {
    server agrisense-1:8000;
    server agrisense-2:8000;
    server agrisense-3:8000;
}

server {
    listen 80;
    server_name agrisense.example.com;
    
    location / {
        proxy_pass http://agrisense;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /health {
        proxy_pass http://agrisense;
        access_log off;
    }
}
```

### **CI/CD Pipeline (GitHub Actions)**
```yaml
name: Deploy AgriSenseGuardian
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker Image
        run: docker build -t agrisense-guardian:${{ github.sha }} .
      - name: Deploy To Cloud Run
        run: |
          gcloud run deploy agrisense-guardian \
            --image agrisense-guardian:${{ github.sha }} \
            --platform managed \
            --region us-central1
```

---

## 📞 Support & Troubleshooting

### **Common Issues**
1. **Port Already In Use**: Change Host Port Mapping
2. **API Key Errors**: Verify Environment Variables
3. **Memory Issues**: Increase Container Memory Limit
4. **Health Check Fails**: Check Application Startup Time

### **Getting Help**
- **GitHub Issues**: https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN/issues
- **Email Support**: i8o8iworkstation@outlook.com
- **Documentation**: See `Docs/` Folder For Detailed Guides

---

<div align="center">

**🌾 AgriSenseGuardian — Containerized For Global Impact**

**Built With ❤️ For Indian Farmers & The Global Agricultural Community**

</div>