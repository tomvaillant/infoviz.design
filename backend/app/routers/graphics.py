"""
Graphics router for interacting with the Hugging Face graphics space.
"""
from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies import get_current_user
from app.services.hf_spaces_client import hf_spaces_client
from app.models.graphics import (
    GraphicsExamplesRequest,
    GraphicsExamplesResponse,
)

router = APIRouter()

@router.post("/graphics/examples", response_model=GraphicsExamplesResponse)
async def fetch_graphics_examples(
    request: GraphicsExamplesRequest,
    user: dict = Depends(get_current_user),
):
    """
    Fetch graphics inspiration examples from HF Space.
    Requires authentication.
    """
    result = await hf_spaces_client.fetch_graphics_inspiration(request.query)

    return GraphicsExamplesResponse(
        query=request.query,
        items=result.get("items", []),
        raw_html=result.get("raw_html"),
    )
