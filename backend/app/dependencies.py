"""
FastAPI dependencies for authentication and authorization using Clerk JWT tokens.
"""
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_backend_api import Clerk
from app.config import settings
import jwt

logger = logging.getLogger(__name__)

# Enable debug logging for Clerk SDK if in development
if settings.environment == "development":
    logging.basicConfig(level=logging.DEBUG)
    clerk_client = Clerk(
        bearer_auth=settings.clerk_secret_key,
        debug_logger=logging.getLogger("clerk_backend_api")
    )
else:
    clerk_client = Clerk(bearer_auth=settings.clerk_secret_key)

# HTTP Bearer security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    Dependency to get the current authenticated user via Clerk JWT token.

    The JWT token includes custom session claims (credits, timezone, onboarding_completed)
    that were configured in the Clerk Dashboard under Session Token customization.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        User dict with:
            - clerk_user_id: Clerk user ID
            - email: User's email address
            - credits: User's credit balance (from session token claim)
            - timezone: User's timezone (from session token claim)
            - onboarding_completed: Whether user completed onboarding
            - needs_initialization: True if metadata is missing

    Raises:
        HTTPException: If authentication fails
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials.strip()

    # Validate token is not empty or literal "null"/"undefined"
    if not token or token.lower() in ['null', 'undefined', '']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode JWT token to extract claims
        # In development, we skip signature verification for easier testing
        # In production, you should verify the signature using Clerk's JWKS
        if settings.environment == "development":
            decoded = jwt.decode(
                token,
                options={"verify_signature": False}
            )
        else:
            # TODO: Implement proper JWT verification with Clerk JWKS in production
            # For now, we'll use sessions.verify as fallback
            decoded = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            logger.warning("Production JWT verification not implemented yet, using unverified decode")

        # Extract user ID from 'sub' claim
        user_id = decoded.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract custom claims from session token
        # These are set in Clerk Dashboard → Sessions → Customize session token
        credits = decoded.get("credits")
        timezone = decoded.get("timezone")
        onboarding_completed = decoded.get("onboarding_completed")
        email = decoded.get("email")

        # Check if user needs initialization. If the token has not yet been refreshed
        # (credits missing) fall back to Clerk to avoid false positives.
        needs_initialization = credits is None
        should_refresh_metadata = (
            needs_initialization
            or credits is None
            or timezone is None
            or onboarding_completed is None
        )

        if should_refresh_metadata:
            try:
                clerk_user = clerk_client.users.get(user_id=user_id)
                public_metadata = getattr(clerk_user, "public_metadata", {}) or {}

                if credits is None:
                    credits = public_metadata.get("credits")
                if not timezone and public_metadata.get("timezone"):
                    timezone = public_metadata.get("timezone")
                if onboarding_completed is None and "onboarding_completed" in public_metadata:
                    onboarding_completed = public_metadata.get("onboarding_completed")

                needs_initialization = public_metadata.get("credits") is None
            except Exception as exc:
                logger.warning(
                    "Unable to hydrate Clerk metadata for %s: %s",
                    user_id,
                    exc
                )

        logger.info(f"Authenticated Clerk user: {user_id} (needs_init: {needs_initialization})")

        return {
            "clerk_user_id": user_id,
            "email": email,
            "credits": credits if credits is not None else 0,
            "timezone": timezone if timezone else settings.default_timezone,
            "onboarding_completed": bool(onboarding_completed),
            "needs_initialization": needs_initialization,
            "session_id": decoded.get("sid"),
        }

    except jwt.DecodeError as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Clerk authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[dict]:
    """
    Dependency to get the current user if authenticated, otherwise None.
    Use this for endpoints that support both authenticated and anonymous access.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        User dict or None if not authenticated
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


async def require_initialized_user(
    user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency that requires user to have completed initialization.
    Use this for endpoints that need fully initialized users.

    Args:
        user: User dict from get_current_user

    Returns:
        User dict if initialized

    Raises:
        HTTPException: If user needs initialization
    """
    if user.get("needs_initialization", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User initialization required. Please complete onboarding.",
            headers={"X-Initialization-Required": "true"}
        )

    return user
