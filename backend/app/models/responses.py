"""
API response models for scraper and other endpoints.
"""
from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class CreditChargeRequest(BaseModel):
    """Request to deduct credits for a scrape action."""
    amount: int = Field(..., gt=0, description="Number of credits to deduct")


class CreditBalanceResponse(BaseModel):
    """Response containing updated credit balance."""
    credits: int


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
    status_code: int = 500
