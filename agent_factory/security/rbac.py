"""Role-based access control."""

from enum import Enum
from typing import List, Callable
from functools import wraps
from fastapi import HTTPException, status, Request


class Permission(str, Enum):
    """Permission types."""
    READ_AGENTS = "agents:read"
    WRITE_AGENTS = "agents:write"
    DELETE_AGENTS = "agents:delete"
    READ_WORKFLOWS = "workflows:read"
    WRITE_WORKFLOWS = "workflows:write"
    DELETE_WORKFLOWS = "workflows:delete"
    READ_BLUEPRINTS = "blueprints:read"
    PUBLISH_BLUEPRINTS = "blueprints:publish"
    ADMIN = "admin:*"


class Role(str, Enum):
    """Role types."""
    USER = "user"
    CREATOR = "creator"
    ADMIN = "admin"


# Role to permissions mapping
ROLE_PERMISSIONS = {
    Role.USER: [
        Permission.READ_AGENTS,
        Permission.WRITE_AGENTS,
        Permission.READ_WORKFLOWS,
        Permission.WRITE_WORKFLOWS,
        Permission.READ_BLUEPRINTS,
    ],
    Role.CREATOR: [
        Permission.READ_AGENTS,
        Permission.WRITE_AGENTS,
        Permission.READ_WORKFLOWS,
        Permission.WRITE_WORKFLOWS,
        Permission.READ_BLUEPRINTS,
        Permission.PUBLISH_BLUEPRINTS,
    ],
    Role.ADMIN: [
        Permission.READ_AGENTS,
        Permission.WRITE_AGENTS,
        Permission.DELETE_AGENTS,
        Permission.READ_WORKFLOWS,
        Permission.WRITE_WORKFLOWS,
        Permission.DELETE_WORKFLOWS,
        Permission.READ_BLUEPRINTS,
        Permission.PUBLISH_BLUEPRINTS,
        Permission.ADMIN,
    ],
}


def get_user_permissions(request: Request) -> List[Permission]:
    """
    Get user permissions from request.
    
    Args:
        request: FastAPI request
        
    Returns:
        List of permissions
    """
    # In production, fetch from database based on user_id
    # For now, return default permissions
    user_roles = getattr(request.state, "user_roles", [Role.USER])
    permissions = []
    
    for role in user_roles:
        if role in ROLE_PERMISSIONS:
            permissions.extend(ROLE_PERMISSIONS[role])
    
    return list(set(permissions))


def require_permission(permission: Permission):
    """
    Decorator to require specific permission.
    
    Args:
        permission: Required permission
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request from kwargs
            request = kwargs.get("request")
            if not request:
                # Try to find request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            user_permissions = get_user_permissions(request)
            
            if permission not in user_permissions and Permission.ADMIN not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {permission.value}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role: Role):
    """
    Decorator to require specific role.
    
    Args:
        role: Required role
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            user_roles = getattr(request.state, "user_roles", [])
            
            if role not in user_roles and Role.ADMIN not in user_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role required: {role.value}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
