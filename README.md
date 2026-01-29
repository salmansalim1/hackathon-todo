# Phase 4: Kubernetes Deployment with Minikube

## 🚀 Overview
This phase deploys the Todo Application with AI Chatbot on Kubernetes using Minikube, featuring:
- **2 Frontend replicas** (React app)
- **2 Backend replicas** (Node.js/Express API)
- **PostgreSQL database** (Neon.tech serverless)
- **OpenAI integration** for AI chatbot
- **Helm charts** for simplified deployment
- **Kubernetes Secrets** for secure credential management

## 📋 Prerequisites

Ensure you have the following installed:
- Docker (v20.10+)
- Minikube (v1.25+)
- kubectl (v1.23+)
- Helm 3 (v3.8+)

### Installation Commands (Ubuntu/WSL)
```bash
# Docker
sudo apt update
sudo apt install docker.io -y

# Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## 🏗️ Architecture
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Frontend      │────▶ │    Backend       │────▶ │   PostgreSQL    │
│   (React)       │      │  (Node.js/Express)│      │   (Neon.tech)   │
│   Port: 30000   │      │   Port: 30001    │      │   (External)    │
│   Replicas: 2   │      │   Replicas: 2    │      └─────────────────┘
└─────────────────┘      └──────────────────┘               │
                                  │                          │
                                  ▼                          │
                         ┌─────────────────┐                │
                         │   OpenAI API    │◀───────────────┘
                         │   (AI Chatbot)  │
                         └─────────────────┘
```

## 📁 Project Structure
```
phase4/
├── backend/                    # Backend application
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── frontend/                   # Frontend application
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── k8s/
│   └── base/
│       ├── backend-deployment.yaml
│       ├── backend-service.yaml
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml
│       └── secrets.yaml
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── .helmignore
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           └── secrets.yaml
├── README.md
└── DEPLOYMENT.md
```

## 🚀 Quick Start

### 1. Start Minikube
```bash
minikube start --driver=docker --memory=4096 --cpus=2
```

### 2. Build Docker Images
```bash
cd /home/salman/hackathon-todo/phase4

# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend
```

### 3. Load Images into Minikube
```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 4. Deploy Using kubectl
```bash
# Create namespace
kubectl create namespace todo-app

# Apply all manifests
kubectl apply -f k8s/base/

# Wait for pods to be ready
kubectl get pods -n todo-app -w
```

### 5. Deploy Using Helm (Alternative)
```bash
cd /home/salman/hackathon-todo/phase4

# Install the chart
helm install todo-app ./helm/todo-app

# Check status
helm status todo-app
```

### 6. Access the Application
```bash
# Access frontend (keep terminal open)
minikube service todo-frontend-service -n todo-app

# Access backend (in new terminal)
minikube service todo-backend-service -n todo-app --url
```

Open the frontend URL in your browser to use the application!

## 🔍 Verification Commands

### Check All Resources
```bash
# View all pods
kubectl get pods -n todo-app

# View all services
kubectl get svc -n todo-app

# View deployments
kubectl get deployments -n todo-app

# View secrets
kubectl get secrets -n todo-app
```

### Check Logs
```bash
# Backend logs
kubectl logs -n todo-app -l app=todo-backend --tail=100

# Frontend logs
kubectl logs -n todo-app -l app=todo-frontend --tail=100

# Follow logs in real-time
kubectl logs -f -n todo-app deployment/todo-backend
```

### Describe Resources
```bash
# Describe backend pod
kubectl describe pod -n todo-app -l app=todo-backend

# Describe frontend service
kubectl describe service -n todo-app todo-frontend-service
```

## 🔄 Update Deployment

### Update Backend Code
```bash
# 1. Make changes to backend code
cd /home/salman/hackathon-todo/phase4/backend

# 2. Rebuild image
docker build -t todo-backend:latest .

# 3. Load into Minikube
minikube image load todo-backend:latest

# 4. Restart deployment
kubectl rollout restart deployment todo-backend -n todo-app

# 5. Check rollout status
kubectl rollout status deployment todo-backend -n todo-app
```

### Update Frontend Code
```bash
# 1. Make changes to frontend code
cd /home/salman/hackathon-todo/phase4/frontend

# 2. Rebuild image
docker build -t todo-frontend:latest .

# 3. Load into Minikube
minikube image load todo-frontend:latest

# 4. Restart deployment
kubectl rollout restart deployment todo-frontend -n todo-app

# 5. Check rollout status
kubectl rollout status deployment todo-frontend -n todo-app
```

## 📊 Scaling

### Scale Deployments
```bash
# Scale backend to 3 replicas
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Scale frontend to 4 replicas
kubectl scale deployment todo-frontend --replicas=4 -n todo-app

# Verify scaling
kubectl get pods -n todo-app
```

### Auto-scaling (Optional)
```bash
# Enable metrics server
minikube addons enable metrics-server

# Create HPA for backend
kubectl autoscale deployment todo-backend --cpu-percent=70 --min=2 --max=5 -n todo-app

# Check HPA status
kubectl get hpa -n todo-app
```

## 🐛 Troubleshooting

### Pods Not Starting
```bash
# Check pod status
kubectl get pods -n todo-app

# Describe problematic pod
kubectl describe pod <pod-name> -n todo-app

# Check pod logs
kubectl logs <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Image Pull Errors
```bash
# Verify images are loaded in Minikube
minikube image ls | grep todo

# Reload images
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Check if pods are running
kubectl get pods -n todo-app -o wide

# Verify service configuration
kubectl describe service todo-frontend-service -n todo-app
```

### Database Connection Issues
```bash
# Check secrets
kubectl get secret todo-secrets -n todo-app -o yaml

# Verify environment variables in pod
kubectl exec -n todo-app deployment/todo-backend -- env | grep DATABASE

# Test database connectivity from pod
kubectl exec -it -n todo-app deployment/todo-backend -- sh
# Inside pod:
# node -e "console.log(process.env.DATABASE_URL)"
```

## 🧹 Cleanup

### Delete All Resources
```bash
# Using kubectl
kubectl delete namespace todo-app

# Using Helm
helm uninstall todo-app
```

### Stop Minikube
```bash
minikube stop
```

### Delete Minikube Cluster
```bash
minikube delete
```

## 🔗 Related Links

- **Phase 3 Backend (Render)**: https://hackathon-todo-backend-jjuf.onrender.com
- **Phase 3 Frontend (Vercel)**: https://hackathon-todo-chatbot.vercel.app/
- **GitHub Repository**: https://github.com/salmansalim1/hackathon-todo

## 📝 Notes

- Frontend runs on NodePort 30000
- Backend runs on NodePort 30001
- Database is hosted on Neon.tech (PostgreSQL serverless)
- OpenAI API is used for AI chatbot functionality
- All sensitive credentials are stored in Kubernetes Secrets

## 🎯 Features Demonstrated

✅ Multi-container deployment
✅ Service discovery and networking
✅ Secrets management
✅ Replica sets and scaling
✅ Health checks and monitoring
✅ Helm package management
✅ External database integration
✅ AI/ML service integration

## 👤 Author

**Salman Salim**
- GitHub: [@salmansalim1](https://github.com/salmansalim1)

---

**Happy Deploying! 🚀**
