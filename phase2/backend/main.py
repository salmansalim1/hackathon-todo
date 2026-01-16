"""
FastAPI Backend for Todo Application - Phase II
With Better Auth JWT Integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
from contextlib import asynccontextmanager
import os

from db import get_session, create_db_and_tables
from models import Task, TaskCreate, TaskUpdate
from auth import verify_jwt_token, verify_user_access

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    create_db_and_tables()
    yield

app = FastAPI(
    title="Todo API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        os.getenv("FRONTEND_URL", "http://localhost:3000")  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Todo API is running"}

@app.get("/api/{user_id}/tasks", response_model=List[Task])
def get_tasks(
    user_id: str,
    status: Optional[str] = "all",
    session: Session = Depends(get_session),
    auth_user: dict = Depends(verify_jwt_token)
):
    """
    Get all tasks for the authenticated user
    Query params: status (all | pending | completed)
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, auth_user)
    
    # Build query
    query = select(Task).where(Task.user_id == user_id)
    
    # Filter by status if specified
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
    
    # Execute and return
    tasks = session.exec(query).all()
    return tasks

@app.post("/api/{user_id}/tasks", response_model=Task)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    auth_user: dict = Depends(verify_jwt_token)
):
    """Create a new task for the authenticated user"""
    verify_user_access(user_id, auth_user)
    
    # Create task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task

@app.get("/api/{user_id}/tasks/{task_id}", response_model=Task)
def get_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    auth_user: dict = Depends(verify_jwt_token)
):
    """Get a specific task by ID"""
    verify_user_access(user_id, auth_user)
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@app.put("/api/{user_id}/tasks/{task_id}", response_model=Task)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    auth_user: dict = Depends(verify_jwt_token)
):
    """Update a task's title or description"""
    verify_user_access(user_id, auth_user)
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task

@app.delete("/api/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    auth_user: dict = Depends(verify_jwt_token)
):
    """Delete a task"""
    verify_user_access(user_id, auth_user)
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    
    return {"status": "deleted", "task_id": task_id}

@app.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=Task)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    auth_user: dict = Depends(verify_jwt_token)
):
    """Toggle task completion status"""
    verify_user_access(user_id, auth_user)
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = not task.completed
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task
