"""Payments API routes."""

from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any, Optional
from pydantic import BaseModel

from agent_factory.payments.stripe_client import create_checkout_session, handle_webhook
from agent_factory.payments.subscriptions import create_subscription, cancel_subscription, get_subscription
from agent_factory.payments.revenue_sharing import calculate_revenue_share, distribute_payment
from agent_factory.security.auth import get_current_user
from agent_factory.security.rbac import require_permission, Permission

router = APIRouter()


class CheckoutRequest(BaseModel):
    """Checkout request."""
    blueprint_id: str
    success_url: str
    cancel_url: str


class SubscriptionRequest(BaseModel):
    """Subscription request."""
    customer_id: str
    blueprint_id: str
    price_id: str


@router.post("/checkout", response_model=Dict[str, Any])
async def create_checkout(
    request: CheckoutRequest,
    user=Depends(get_current_user)
):
    """Create checkout session for blueprint purchase."""
    require_permission(Permission.READ_BLUEPRINTS)(lambda: None)()
    
    from agent_factory.marketplace.search import get_blueprint_details
    blueprint = get_blueprint_details(request.blueprint_id)
    
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    price = blueprint.get("price", 0.0)
    if price <= 0:
        raise HTTPException(status_code=400, detail="Blueprint is free")
    
    customer_email = user.email if hasattr(user, 'email') else None
    
    session = create_checkout_session(
        blueprint_id=request.blueprint_id,
        price=price,
        success_url=request.success_url,
        cancel_url=request.cancel_url,
        customer_email=customer_email
    )
    
    return session


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    result = handle_webhook(request)
    return result


@router.post("/subscription", response_model=Dict[str, Any])
async def create_subscription_endpoint(
    request: SubscriptionRequest,
    user=Depends(get_current_user)
):
    """Create subscription for blueprint."""
    require_permission(Permission.READ_BLUEPRINTS)(lambda: None)()
    
    subscription = create_subscription(
        customer_id=request.customer_id,
        blueprint_id=request.blueprint_id,
        price_id=request.price_id
    )
    
    return subscription


@router.post("/subscription/{subscription_id}/cancel", response_model=Dict[str, Any])
async def cancel_subscription_endpoint(
    subscription_id: str,
    user=Depends(get_current_user)
):
    """Cancel subscription."""
    require_permission(Permission.READ_BLUEPRINTS)(lambda: None)()
    
    result = cancel_subscription(subscription_id)
    return result


@router.get("/subscription/{subscription_id}", response_model=Dict[str, Any])
async def get_subscription_endpoint(
    subscription_id: str,
    user=Depends(get_current_user)
):
    """Get subscription details."""
    require_permission(Permission.READ_BLUEPRINTS)(lambda: None)()
    
    subscription = get_subscription(subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return subscription


@router.get("/revenue-share/{blueprint_id}", response_model=Dict[str, Any])
async def get_revenue_share(
    blueprint_id: str,
    amount: float,
    user=Depends(get_current_user)
):
    """Calculate revenue share for blueprint."""
    require_permission(Permission.READ_BLUEPRINTS)(lambda: None)()
    
    revenue_share = calculate_revenue_share(amount)
    return revenue_share
