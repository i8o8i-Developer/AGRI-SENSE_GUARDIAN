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

Create A `.env` File With Required API Keys:

```env
# Google Gemini AI (Required)
GOOGLE_API_KEY=your_google_api_key_here

# Weather Data (Optional - Uses Free Open-Meteo If Not Provided)
OPENWEATHER_API_KEY=your_openweather_key

# Email Notifications (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=your_email@gmail.com
SENDER_NAME=AgriSenseGuardian

# Enhanced Data Sources (Optional)
COPERNICUS_API_KEY=your_copernicus_uid:api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# Application Configuration
API_HOST=0.0.0.0
API_PORT=8000
START_A2A_ON_STARTUP=true
LOG_LEVEL=INFO
```

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

### **Google Cloud Run (Recommended)**

#### **Deploy To Cloud Run**
```bash
# Build And Push To Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/agrisense-guardian

# Deploy To Cloud Run
gcloud run deploy agrisense-guardian \
  --image gcr.io/PROJECT_ID/agrisense-guardian \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key \
  --port 8000 \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

#### **Environment Variables Setup**
```bash
# Set Required Environment Variables
gcloud run services update agrisense-guardian \
  --set-env-vars GOOGLE_API_KEY=your_api_key,START_A2A_ON_STARTUP=true \
  --region us-central1
```

### **AWS Fargate**

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
        {"name": "GOOGLE_API_KEY", "value": "your_key"},
        {"name": "START_A2A_ON_STARTUP", "value": "true"}
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

### **Azure Container Instances**

```bash
az container create \
  --resource-group agrisense-rg \
  --name agrisense-guardian \
  --image your-registry.azurecr.io/agrisense-guardian:latest \
  --dns-name-label agrisense-guardian \
  --ports 8000 \
  --environment-variables GOOGLE_API_KEY=your_key START_A2A_ON_STARTUP=true \
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