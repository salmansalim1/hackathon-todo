from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import get_session
from models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

@router.post("/signup", response_model=UserResponse)
def signup(request: SignupRequest, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = pwd_context.hash(request.password)
    
    # Create new user
    new_user = User(
        email=request.email,
        name=request.name,
        hashed_password=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name
    )

@router.post("/signin", response_model=UserResponse)
def signin(request: SigninRequest, session: Session = Depends(get_session)):
    # Find user
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name
    )
