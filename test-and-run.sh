#!/bin/bash

set -e

echo "========================================"
echo "Todo App - Phase 4 Testing & Deployment"
echo "========================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo -e "${RED}❌ Minikube is not running!${NC}"
    echo "Start it with: minikube start"
    exit 1
fi

echo -e "${GREEN}✅ Minikube is running${NC}"

# Check if namespace exists
if ! kubectl get namespace todo-app &> /dev/null; then
    echo -e "${RED}❌ Namespace todo-app not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Namespace exists${NC}"

# Check pod status
echo ""
echo "Checking pod status..."
kubectl get pods -n todo-app

# Wait for all pods to be ready
echo ""
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=60s
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=60s

echo -e "${GREEN}✅ All pods are ready${NC}"

# Check services
echo ""
echo "Checking services..."
kubectl get svc -n todo-app

# Kill existing port-forwards
echo ""
echo "Stopping existing port forwards..."
pkill -f "kubectl port-forward" 2>/dev/null || true
sleep 2

# Start port-forwards with correct ports
echo ""
echo "Starting port forwards..."
kubectl port-forward -n todo-app svc/todo-backend-service 8000:8000 > /dev/null 2>&1 &
sleep 2
kubectl port-forward -n todo-app svc/todo-frontend-service 3000:3000 > /dev/null 2>&1 &
sleep 2

echo -e "${GREEN}✅ Port forwards started${NC}"

# Test backend health
echo ""
echo "Testing backend health..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
    curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    exit 1
fi

# Test frontend
echo ""
echo "Testing frontend..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 304 ]; then
    echo -e "${GREEN}✅ Frontend is accessible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend returned HTTP $HTTP_CODE${NC}"
fi

# Test Helm
echo ""
echo "Checking Helm deployment..."
if helm list -n todo-app 2>/dev/null | grep -q todo-app; then
    echo -e "${GREEN}✅ Helm chart is deployed${NC}"
    helm list -n todo-app
else
    echo -e "${YELLOW}⚠️  Helm chart not found (deployment via kubectl is OK)${NC}"
fi

# Summary
echo ""
echo "========================================"
echo -e "${GREEN}✅ Phase 4 Deployment Test Complete${NC}"
echo "========================================"
echo ""
echo "Access your application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  Backend Health: http://localhost:8000/health"
echo ""
echo "From Windows (use Minikube IP):"
MINIKUBE_IP=$(minikube ip)
echo "  Frontend: http://$MINIKUBE_IP:30000"
echo "  Backend:  http://$MINIKUBE_IP:30001"
echo ""
echo "To stop port forwards:"
echo "  pkill -f 'kubectl port-forward'"
echo ""
echo "To view logs:"
echo "  kubectl logs -n todo-app -l app=todo-backend"
echo "  kubectl logs -n todo-app -l app=todo-frontend"
echo ""
