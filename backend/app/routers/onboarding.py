"""
User onboarding router for initializing new user metadata.
"""
import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.dependencies import get_current_user, clerk_client
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class InitializeUserRequest(BaseModel):
    """Request model for user initialization."""
    timezone: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="IANA timezone identifier (e.g., 'America/New_York', 'Europe/London')"
    )


class UserMetadataResponse(BaseModel):
    """Response model for user metadata."""
    clerk_user_id: str
    email: str
    credits: int
    timezone: str
    onboarding_completed: bool
    initialized_at: str | None = None


@router.post("/initialize", response_model=UserMetadataResponse)
async def initialize_user(
    payload: InitializeUserRequest,
    user: dict = Depends(get_current_user)
):
    """
    Initialize or update a new user's metadata after signup.

    This endpoint should be called once after user registration to set up:
    - Initial credits (default: 100)
    - User's timezone
    - Onboarding completion flag

    This endpoint is idempotent. If the user is already partially or fully
    initialized, it will merge the new data, ensuring the timezone from the
    payload is always respected.

    Args:
        payload: Initialization request with timezone
        user: Current authenticated user (from JWT token)

    Returns:
        User metadata including credits, timezone, and onboarding status

    Raises:
        HTTPException: If timezone is invalid or initialization fails
    """
    clerk_user_id = user.get("clerk_user_id")

    # Validate timezone identifier first
    try:
        ZoneInfo(payload.timezone)
    except Exception as e:
        logger.error(f"Invalid timezone '{payload.timezone}': {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timezone identifier: {payload.timezone}",
        )

    try:
        clerk_user = clerk_client.users.get(user_id=clerk_user_id)
    except Exception as exc:
        logger.error(f"Failed to load Clerk user {clerk_user_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to load user profile from Clerk. Please retry in a moment.",
        )

    public_metadata = getattr(clerk_user, "public_metadata", {}) or {}
    email_address = (
        clerk_user.email_addresses[0].email_address
        if getattr(clerk_user, "email_addresses", None)
        else user.get("email", "")
    )

    try:
        # Prepare metadata, merging with any existing data but ensuring
        # the timezone from the payload and onboarding flags are authoritative.
        initialized_at = public_metadata.get("initialized_at") or datetime.now().isoformat()
        
        final_metadata = {
            **public_metadata,
            "credits": public_metadata.get("credits", settings.default_credits),
            "timezone": payload.timezone,
            "onboarding_completed": True,
            "initialized_at": initialized_at
        }

        # Update user metadata in Clerk
        updated_user = clerk_client.users.update_metadata(
            user_id=clerk_user_id,
            public_metadata=final_metadata
        )

        logger.info(f"✅ Initialized/updated user {clerk_user_id} with metadata: {final_metadata}")

        # Small delay to allow Clerk edge caches to settle
        await asyncio.sleep(0.2)

        confirmed_email = (
            updated_user.email_addresses[0].email_address
            if getattr(updated_user, "email_addresses", None)
            else email_address
        )

        return UserMetadataResponse(
            clerk_user_id=clerk_user_id,
            email=confirmed_email,
            credits=final_metadata["credits"],
            timezone=final_metadata["timezone"],
            onboarding_completed=final_metadata["onboarding_completed"],
            initialized_at=final_metadata["initialized_at"]
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"❌ Failed to initialize user {clerk_user_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize user. Please try again."
        )


@router.get("/status")
async def get_onboarding_status(user: dict = Depends(get_current_user)):
    """
    Check if user has completed onboarding/initialization.

    Returns:
        Onboarding status and metadata information
    """
    return {
        "needs_initialization": user.get("needs_initialization", False),
        "onboarding_completed": user.get("onboarding_completed", False),
        "credits": user.get("credits"),
        "timezone": user.get("timezone"),
        "metadata": {
            "from_jwt_token": True,
            "clerk_user_id": user.get("clerk_user_id"),
            "email": user.get("email")
        }
    }


@router.get("/metadata")
async def get_user_metadata(user: dict = Depends(get_current_user)):
    """
    Get detailed user metadata for debugging and display purposes.

    This endpoint fetches fresh metadata from Clerk API and compares it
    with the data from the JWT token to help diagnose any sync issues.

    Returns:
        User metadata from both JWT token and Clerk API
    """
    clerk_user_id = user.get("clerk_user_id")

    try:
        # Fetch fresh data from Clerk API
        clerk_user = clerk_client.users.get(user_id=clerk_user_id)

        return {
            "clerk_user_id": clerk_user_id,
            "email": clerk_user.email_addresses[0].email_address if clerk_user.email_addresses else "",
            "from_jwt_token": {
                "credits": user.get("credits"),
                "timezone": user.get("timezone"),
                "onboarding_completed": user.get("onboarding_completed"),
                "needs_initialization": user.get("needs_initialization")
            },
            "from_clerk_api": clerk_user.public_metadata,
            "sync_status": {
                "in_sync": user.get("credits") == clerk_user.public_metadata.get("credits"),
                "note": "JWT token updates after next sign-in or token refresh"
            }
        }
    except Exception as exc:
        logger.error(f"Failed to fetch metadata for {clerk_user_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user metadata"
        )
