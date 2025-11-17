"""
Authentication router for handling auth-related endpoints.
"""
import logging
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.dependencies import get_current_user, get_optional_user, clerk_client, require_initialized_user

logger = logging.getLogger(__name__)

router = APIRouter()


class TimezoneUpdateRequest(BaseModel):
    timezone: str = Field(..., min_length=2, max_length=120)


@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Get current authenticated user's information from Clerk.

    Returns:
        User information including clerk_user_id, email, credits, and timezone
    """
    return {
        "user": user,
        "authenticated": True,
    }


@router.get("/status")
async def get_auth_status(user: dict = Depends(get_optional_user)):
    """
    Get authentication status (works for both authenticated and anonymous users).

    Returns:
        Authentication status
    """
    if user:
        return {
            "authenticated": True,
            "user": {
                "clerk_user_id": user.get("clerk_user_id"),
                "email": user.get("email"),
                "credits": user.get("credits"),
                "timezone": user.get("timezone"),
                "needs_initialization": user.get("needs_initialization", False),
                "onboarding_completed": user.get("onboarding_completed", False),
            },
        }
    else:
        return {
            "authenticated": False,
            "user": None,
        }


@router.post("/timezone")
async def update_timezone(
    payload: TimezoneUpdateRequest,
    user: dict = Depends(require_initialized_user)
):
    """
    Update the authenticated user's timezone in Clerk public metadata.

    Note: Changes will be reflected in the JWT token after the next token refresh
    or user sign-in, as the JWT contains a snapshot of metadata at token creation time.
    """
    # Validate timezone identifier
    try:
        ZoneInfo(payload.timezone)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid timezone identifier",
        )

    clerk_user_id = user.get("clerk_user_id")

    try:
        # Use update_metadata to merge the timezone into public_metadata
        # This avoids fetching the user first and prevents race conditions
        clerk_client.users.update_metadata(
            user_id=clerk_user_id,
            public_metadata={"timezone": payload.timezone}
        )

        logger.info(f"Updated timezone for user {clerk_user_id} to {payload.timezone}")

        return {
            "success": True,
            "timezone": payload.timezone,
            "note": "Changes will appear in new tokens after refresh"
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Failed to update timezone for {clerk_user_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update timezone",
        )
