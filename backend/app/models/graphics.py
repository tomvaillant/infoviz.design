"""
Pydantic models for graphics-related endpoints.
"""
from typing import Optional, List
from pydantic import BaseModel, Field

class GraphicsExamplesRequest(BaseModel):
    """Request model for fetching graphics examples."""
    query: str = Field(
        ...,
        min_length=1,
        description="Search query for graphics examples"
    )

class GraphicsExample(BaseModel):
    """Individual graphics example/card."""
    title: str
    source: Optional[str] = None
    date: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None

class GraphicsExamplesResponse(BaseModel):
    """Response model for graphics examples."""
    query: str = Field(..., description="The original search query")
    items: List[GraphicsExample] = Field(
        default_factory=list,
        description="List of graphics examples"
    )
    raw_html: Optional[str] = Field(
        None,
        description="Raw HTML from Gradio space (for debugging)"
    )