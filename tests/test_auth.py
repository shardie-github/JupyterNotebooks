"""Tests for authentication."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
import jwt

from agent_factory.security.auth import (
    create_access_token,
    verify_token,
    TokenData,
    SECRET_KEY,
    ALGORITHM,
)


@pytest.mark.unit
def test_create_access_token():
    """Test creating an access token."""
    data = {"sub": "user-123", "email": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    # Verify token can be decoded
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user-123"
    assert payload["email"] == "test@example.com"


@pytest.mark.unit
def test_create_access_token_with_expiry():
    """Test creating token with custom expiry."""
    data = {"sub": "user-123"}
    expires_delta = timedelta(minutes=60)
    token = create_access_token(data, expires_delta=expires_delta)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp_time = datetime.fromtimestamp(payload["exp"])
    assert exp_time > datetime.utcnow() + timedelta(minutes=59)


@pytest.mark.unit
def test_verify_token_valid():
    """Test verifying a valid token."""
    data = {"sub": "user-123", "email": "test@example.com"}
    token = create_access_token(data)
    
    token_data = verify_token(token)
    
    assert isinstance(token_data, TokenData)
    assert token_data.user_id == "user-123"
    assert token_data.email == "test@example.com"


@pytest.mark.unit
def test_verify_token_expired():
    """Test verifying an expired token."""
    data = {"sub": "user-123"}
    expires_delta = timedelta(seconds=-1)  # Already expired
    token = create_access_token(data, expires_delta=expires_delta)
    
    with pytest.raises(Exception):  # Should raise HTTPException
        verify_token(token)


@pytest.mark.unit
def test_verify_token_invalid():
    """Test verifying an invalid token."""
    invalid_token = "invalid.token.here"
    
    with pytest.raises(Exception):  # Should raise HTTPException
        verify_token(invalid_token)


@pytest.mark.unit
def test_verify_token_missing_sub():
    """Test verifying token without subject."""
    data = {"email": "test@example.com"}  # Missing 'sub'
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(Exception):  # Should raise HTTPException
        verify_token(token)
