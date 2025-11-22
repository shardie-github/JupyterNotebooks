"""JWT authentication."""

import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    """User model."""
    id: str
    email: str
    roles: list[str] = []
    permissions: list[str] = []


class TokenData(BaseModel):
    """Token data model."""
    user_id: Optional[str] = None
    email: Optional[str] = None


security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Token payload data
        expires_delta: Optional expiration delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Token data
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class JWTBearer(HTTPBearer):
    """JWT Bearer token authentication."""
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request, credentials: HTTPAuthorizationCredentials = Security(security)):
        """Verify JWT token."""
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated"
            )
        
        token = credentials.credentials
        token_data = verify_token(token)
        
        # Store user info in request state
        request.state.user_id = token_data.user_id
        request.state.user_email = token_data.email
        
        return token_data


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    """
    Get current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        User object
    """
    token = credentials.credentials
    token_data = verify_token(token)
    
    # Fetch user from database
    from agent_factory.database.session import get_db
    from agent_factory.database.models import User as UserModel
    
    db = next(get_db())
    try:
        user_model = db.query(UserModel).filter(UserModel.id == token_data.user_id).first()
        
        if not user_model:
            # Return anonymous user if not found
            return User(
                id=token_data.user_id or "anonymous",
                email=token_data.email or "anonymous@example.com",
                roles=["user"],
                permissions=["read", "write"]
            )
        
        return User(
            id=user_model.id,
            email=user_model.email,
            roles=user_model.roles or [],
            permissions=user_model.permissions or []
        )
    finally:
        db.close()
