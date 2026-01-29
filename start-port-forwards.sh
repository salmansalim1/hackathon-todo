#!/bin/bash

echo "Starting port forwards for Todo App..."

# Kill any existing port-forwards
pkill -f "kubectl port-forward" 2>/dev/null || true
sleep 1

# Start backend port-forward
kubectl port-forward -n todo-app svc/todo-backend-service 8000:8000 > /dev/null 2>&1 &
echo "✅ Backend available at: http://localhost:8000"

# Start frontend port-forward  
kubectl port-forward -n todo-app svc/todo-frontend-service 3000:3000 > /dev/null 2>&1 &
echo "✅ Frontend available at: http://localhost:3000"

echo ""
echo "Port forwards running in background."
echo ""
echo "Test backend: curl http://localhost:8000/health"
echo "Test frontend: curl http://localhost:3000"
echo ""
echo "To stop: pkill -f 'kubectl port-forward'"
