"""
JWT Authentication for FastAPI Backend
Integrates with Better Auth tokens from Next.js frontend
"""
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os
from datetime import datetime

security = HTTPBearer()

# Get secret from environment - MUST match Better Auth secret
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-this")
JWT_ALGORITHM = "HS256"

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Verify JWT token from Authorization: Bearer <token> header
    Returns decoded token payload with user information
    """
    try:
        token = credentials.credentials
        
        # Decode and verify JWT
        payload = jwt.decode(
            token, 
            JWT_SECRET, 
            algorithms=[JWT_ALGORITHM]
        )
        
        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        # Extract user info
        user_id = payload.get("sub") or payload.get("userId")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "name": payload.get("name")
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

def verify_user_access(user_id_from_path: str, auth_user: dict) -> bool:
    """
    Verify that the authenticated user matches the user_id in the URL path
    Prevents users from accessing other users' data
    """
    if auth_user["user_id"] != user_id_from_path:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this user's data"
        )
    return True
