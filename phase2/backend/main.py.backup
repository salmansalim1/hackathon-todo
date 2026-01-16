from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager
import os
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing import Optional

from database import init_db, get_session
from models import User, Task

# JWT Configuration
SECRET_KEY = "9be022a8bfd761d7eb7ca5a3ee84acbf620c7b99308ae9aceb4cad3224fe1bc6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    init_db()
    yield

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",  # Allow all origins for now - will restrict after Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Auth Models ====================

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: dict
    token: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# ==================== Auth Utilities ====================

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str) -> str:
    """Create JWT access token"""
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(
    authorization: str = Header(None),
    session: Session = Depends(get_session)
) -> User:
    """Get current authenticated user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_token(token)
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# ==================== Root & Health Check ====================

@app.get("/")
async def root():
    return {
        "message": "Todo API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check(session: Session = Depends(get_session)):
    """Health check endpoint"""
    try:
        # Test database connection
        session.exec(select(User).limit(1))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# ==================== Auth Endpoints ====================

@app.post("/api/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, session: Session = Depends(get_session)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == request.email)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = hash_password(request.password)
        user = User(
            email=request.email,
            password=hashed_password,
            name=request.name
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Generate token
        token = create_access_token(user.id)
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@app.post("/api/auth/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, session: Session = Depends(get_session)):
    """Sign in existing user"""
    try:
        # Find user
        user = session.exec(
            select(User).where(User.email == request.email)
        ).first()
        
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate token
        token = create_access_token(user.id)
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signin error: {e}")
        raise HTTPException(status_code=500, detail=f"Signin failed: {str(e)}")

# ==================== Task Endpoints ====================

@app.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    status: str = "all",
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all tasks for authenticated user"""
    # Verify user_id matches authenticated user
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Build query
    query = select(Task).where(Task.user_id == user_id)
    
    if status == "completed":
        query = query.where(Task.completed == True)
    elif status == "pending":
        query = query.where(Task.completed == False)
    
    tasks = session.exec(query).all()
    return tasks

@app.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task"""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        new_task = Task(
            user_id=user_id,
            title=task.title,
            description=task.description
        )
        
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        
        return new_task
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@app.get("/api/{user_id}/tasks/{task_id}")
async def get_task(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get task details"""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@app.put("/api/{user_id}/tasks/{task_id}")
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task"""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.completed is not None:
            task.completed = task_update.completed
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return task
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@app.delete("/api/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task"""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

@app.patch("/api/{user_id}/tasks/{task_id}/complete")
async def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle task completion status"""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return task
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to toggle task: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
