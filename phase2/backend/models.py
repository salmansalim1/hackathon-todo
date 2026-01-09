from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional
import uuid

def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return str(uuid.uuid4())

class User(SQLModel, table=True):
    """User model for authentication"""
    __tablename__ = "users"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str  # Hashed password
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    """Task model"""
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
