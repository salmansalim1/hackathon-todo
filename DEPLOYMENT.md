# Detailed Deployment Guide

## Pre-Deployment Checklist

- [ ] Minikube is installed and running
- [ ] Docker is installed and running
- [ ] kubectl is configured
- [ ] Helm 3 is installed
- [ ] Phase 3 code is available in `/home/salman/hackathon-todo/phase3`

## Step-by-Step Deployment

### Step 1: Prepare Environment
```bash
# Start Minikube with sufficient resources
minikube start --driver=docker --memory=4096 --cpus=2

# Verify Minikube is running
minikube status

# Check kubectl connection
kubectl cluster-info
```

### Step 2: Prepare Project Directory
```bash
# Navigate to phase4 directory
cd /home/salman/hackathon-todo/phase4

# Verify directory structure
ls -la
```

### Step 3: Build Docker Images
```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Verify images
docker images | grep todo
```

### Step 4: Load Images into Minikube
```bash
# Load backend image
minikube image load todo-backend:latest

# Load frontend image
minikube image load todo-frontend:latest

# Verify images in Minikube
minikube image ls | grep todo
```

### Step 5: Create Kubernetes Resources
```bash
# Create namespace
kubectl create namespace todo-app

# Apply secrets
kubectl apply -f k8s/base/secrets.yaml

# Apply backend resources
kubectl apply -f k8s/base/backend-deployment.yaml
kubectl apply -f k8s/base/backend-service.yaml

# Apply frontend resources
kubectl apply -f k8s/base/frontend-deployment.yaml
kubectl apply -f k8s/base/frontend-service.yaml
```

### Step 6: Verify Deployment
```bash
# Check all resources
kubectl get all -n todo-app

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=300s

# Check pod status
kubectl get pods -n todo-app
```

Expected output:
```
NAME                             READY   STATUS    RESTARTS   AGE
todo-backend-xxxxxxxxx-xxxxx     1/1     Running   0          2m
todo-backend-xxxxxxxxx-xxxxx     1/1     Running   0          2m
todo-frontend-xxxxxxxxx-xxxxx    1/1     Running   0          2m
todo-frontend-xxxxxxxxx-xxxxx    1/1     Running   0          2m
```

### Step 7: Access Services
```bash
# Get frontend URL
minikube service todo-frontend-service -n todo-app

# In new terminal, get backend URL
minikube service todo-backend-service -n todo-app --url
```

### Step 8: Test Application
```bash
# Test backend health endpoint
BACKEND_URL=$(minikube service todo-backend-service -n todo-app --url)
curl $BACKEND_URL/health

# Expected response: {"status":"healthy"}
```

## Alternative: Helm Deployment

### Deploy with Helm
```bash
cd /home/salman/hackathon-todo/phase4

# Lint chart
helm lint helm/todo-app

# Dry run (test without deploying)
helm install todo-app ./helm/todo-app --dry-run --debug

# Install chart
helm install todo-app ./helm/todo-app

# Check status
helm status todo-app

# List releases
helm list
```

### Upgrade with Helm
```bash
# After making changes to values.yaml or templates
helm upgrade todo-app ./helm/todo-app

# Rollback if needed
helm rollback todo-app
```

## Monitoring and Maintenance

### Real-time Monitoring
```bash
# Watch pods
kubectl get pods -n todo-app -w

# Stream backend logs
kubectl logs -f -n todo-app -l app=todo-backend

# Stream frontend logs
kubectl logs -f -n todo-app -l app=todo-frontend

# Monitor resource usage (requires metrics-server)
kubectl top pods -n todo-app
```

### Health Checks
```bash
# Check backend health
kubectl exec -n todo-app deployment/todo-backend -- wget -qO- localhost:5000/health

# Check frontend
kubectl exec -n todo-app deployment/todo-frontend -- wget -qO- localhost:3000
```

## Updating the Application

### Update Backend
```bash
# 1. Make code changes
cd /home/salman/hackathon-todo/phase4/backend

# 2. Rebuild image
docker build -t todo-backend:latest .

# 3. Reload into Minikube
minikube image load todo-backend:latest

# 4. Delete old pods (they will be recreated)
kubectl delete pods -n todo-app -l app=todo-backend

# Or use rolling update
kubectl rollout restart deployment todo-backend -n todo-app

# 5. Watch rollout
kubectl rollout status deployment todo-backend -n todo-app
```

### Update Frontend
```bash
# 1. Make code changes
cd /home/salman/hackathon-todo/phase4/frontend

# 2. Rebuild image
docker build -t todo-frontend:latest .

# 3. Reload into Minikube
minikube image load todo-frontend:latest

# 4. Rolling update
kubectl rollout restart deployment todo-frontend -n todo-app

# 5. Watch rollout
kubectl rollout status deployment todo-frontend -n todo-app
```

## Cleanup Procedures

### Partial Cleanup (Keep namespace)
```bash
# Delete deployments
kubectl delete deployment todo-backend todo-frontend -n todo-app

# Delete services
kubectl delete service todo-backend-service todo-frontend-service -n todo-app

# Delete secrets
kubectl delete secret todo-secrets -n todo-app
```

### Complete Cleanup
```bash
# Delete entire namespace
kubectl delete namespace todo-app

# Or if using Helm
helm uninstall todo-app
```

### Stop Minikube
```bash
# Stop (can restart later)
minikube stop

# Delete (complete removal)
minikube delete
```

## Troubleshooting Guide

### Issue: Pods stuck in "Pending" state
```bash
# Check pod events
kubectl describe pod <pod-name> -n todo-app

# Common causes:
# - Insufficient resources
# - Image pull errors
# - PVC issues
```

**Solution:**
```bash
# Increase Minikube resources
minikube delete
minikube start --driver=docker --memory=8192 --cpus=4
```

### Issue: Pods stuck in "ImagePullBackOff"
```bash
# Check if image exists in Minikube
minikube image ls | grep todo
```

**Solution:**
```bash
# Reload images
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Issue: Backend can't connect to database
```bash
# Check secrets
kubectl get secret todo-secrets -n todo-app -o jsonpath='{.data.DATABASE_URL}' | base64 -d

# Check environment in pod
kubectl exec -n todo-app deployment/todo-backend -- env | grep DATABASE
```

**Solution:**
```bash
# Update secrets
kubectl delete secret todo-secrets -n todo-app
kubectl apply -f k8s/base/secrets.yaml
kubectl rollout restart deployment todo-backend -n todo-app
```

### Issue: Service not accessible
```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Check service details
kubectl describe service todo-frontend-service -n todo-app
```

**Solution:**
```bash
# Verify pod labels match service selectors
kubectl get pods -n todo-app --show-labels

# Restart service
kubectl delete service todo-frontend-service -n todo-app
kubectl apply -f k8s/base/frontend-service.yaml
```

## Production Considerations

### Security

- [ ] Use proper secrets management (e.g., Sealed Secrets, External Secrets)
- [ ] Enable RBAC
- [ ] Use network policies
- [ ] Scan images for vulnerabilities
- [ ] Enable pod security policies

### Monitoring

- [ ] Set up Prometheus and Grafana
- [ ] Configure alerting
- [ ] Enable logging aggregation
- [ ] Set up distributed tracing

### High Availability

- [ ] Use anti-affinity rules
- [ ] Implement proper health checks
- [ ] Configure resource limits
- [ ] Set up autoscaling
- [ ] Use multiple availability zones

---

**Deployment completed! ✅**
