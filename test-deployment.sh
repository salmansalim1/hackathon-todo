#!/bin/bash

echo "=========================================="
echo "   Phase 4 Deployment Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test 1: Minikube
echo -e "${BLUE}[1/6] Checking Minikube Status${NC}"
if minikube status | grep -q "Running"; then
    echo -e "${GREEN}✓ Minikube is running${NC}"
else
    echo -e "${RED}✗ Minikube is not running. Start with: minikube start${NC}"
    exit 1
fi
echo ""

# Test 2: Pods
echo -e "${BLUE}[2/6] Checking Pod Status${NC}"
TOTAL_PODS=$(kubectl get pods --no-headers 2>/dev/null | wc -l)
RUNNING_PODS=$(kubectl get pods --no-headers 2>/dev/null | grep Running | wc -l)

if [ "$RUNNING_PODS" -eq "$TOTAL_PODS" ] && [ "$TOTAL_PODS" -gt 0 ]; then
    echo -e "${GREEN}✓ All $RUNNING_PODS pods are running${NC}"
    kubectl get pods
else
    echo -e "${RED}✗ Only $RUNNING_PODS/$TOTAL_PODS pods running${NC}"
    kubectl get pods
fi
echo ""

# Test 3: Services
echo -e "${BLUE}[3/6] Checking Services${NC}"
if kubectl get service todo-frontend &>/dev/null; then
    echo -e "${GREEN}✓ Frontend service exists${NC}"
else
    echo -e "${YELLOW}⚠ Frontend service not found${NC}"
fi

if kubectl get service todo-backend &>/dev/null; then
    echo -e "${GREEN}✓ Backend service exists${NC}"
else
    echo -e "${YELLOW}⚠ Backend service not found${NC}"
fi
echo ""

# Test 4: Get URLs
echo -e "${BLUE}[4/6] Getting Service URLs${NC}"
FRONTEND_URL=$(minikube service todo-frontend --url 2>/dev/null)
BACKEND_URL=$(minikube service todo-backend --url 2>/dev/null)

if [ -n "$FRONTEND_URL" ]; then
    echo -e "${GREEN}✓ Frontend: $FRONTEND_URL${NC}"
else
    echo -e "${YELLOW}⚠ Frontend URL not available${NC}"
fi

if [ -n "$BACKEND_URL" ]; then
    echo -e "${GREEN}✓ Backend: $BACKEND_URL${NC}"
else
    echo -e "${YELLOW}⚠ Backend URL not available${NC}"
fi
echo ""

# Test 5: Backend Health
if [ -n "$BACKEND_URL" ]; then
    echo -e "${BLUE}[5/6] Testing Backend Health${NC}"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" 2>/dev/null)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✓ Backend healthy (HTTP 200)${NC}"
    elif [ "$HTTP_CODE" = "000" ]; then
        echo -e "${YELLOW}⚠ Could not connect to backend${NC}"
    else
        echo -e "${YELLOW}⚠ Backend returned HTTP $HTTP_CODE${NC}"
    fi
    echo ""
fi

# Test 6: Frontend
if [ -n "$FRONTEND_URL" ]; then
    echo -e "${BLUE}[6/6] Testing Frontend${NC}"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" 2>/dev/null)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✓ Frontend accessible (HTTP 200)${NC}"
    elif [ "$HTTP_CODE" = "000" ]; then
        echo -e "${YELLOW}⚠ Could not connect to frontend${NC}"
    else
        echo -e "${YELLOW}⚠ Frontend returned HTTP $HTTP_CODE${NC}"
    fi
    echo ""
fi

# Summary
echo "=========================================="
echo -e "${YELLOW}SUMMARY${NC}"
echo "=========================================="
echo ""
echo "Deployments:"
kubectl get deployments 2>/dev/null
echo ""
echo "Services:"
kubectl get services 2>/dev/null
echo ""
echo "Access Application:"
echo "  Frontend: minikube service todo-frontend"
echo "  Backend:  minikube service todo-backend --url"
echo ""
echo "View Logs:"
echo "  kubectl logs -l app=todo-frontend --tail=20"
echo "  kubectl logs -l app=todo-backend --tail=20"
echo ""
echo "=========================================="
