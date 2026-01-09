from fastapi import APIRouter, HTTPException, Depends, Header
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, List
from jose import JWTError, jwt
from database import get_session
from models import Task
from datetime import datetime

router = APIRouter()

SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

def get_current_user_id(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    status: Optional[str] = "all",
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Verify user is accessing their own tasks
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Build query
    statement = select(Task).where(Task.user_id == user_id)
    
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    
    tasks = session.exec(statement).all()
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskResponse)
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not task.title or len(task.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if len(task.title) > 200:
        raise HTTPException(status_code=400, detail="Title must be under 200 characters")
    
    new_task = Task(
        user_id=user_id,
        title=task.title.strip(),
        description=task.description.strip() if task.description else None
    )
    
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    
    return new_task

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title is not None:
        if len(task_update.title.strip()) == 0:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task.title = task_update.title.strip()
    
    if task_update.description is not None:
        task.description = task_update.description.strip() if task_update.description else None
    
    if task_update.completed is not None:
        task.completed = task_update.completed
    
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task

@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task
