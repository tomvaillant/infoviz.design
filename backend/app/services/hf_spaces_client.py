"""
Hugging Face Spaces client for calling deployed Gradio apps.
"""
import os
import logging
import asyncio
import json
import base64
from pathlib import Path
from typing import Dict, Any, Optional, List
from gradio_client import Client
from bs4 import BeautifulSoup

from app.config import settings

logger = logging.getLogger(__name__)


class HFSpacesClient:
    """Client for interacting with Hugging Face Spaces via gradio_client."""

    def __init__(self):
        """Initialize HF Spaces client."""
        self.hf_token = settings.huggingface_api_key
        self.space_urls = settings.hf_spaces

    async def fetch_graphics_inspiration(self, query: str) -> Dict[str, Any]:
        """
        Query the GRAPHICS space for inspiration examples.

        Args:
            query: Search query text

        Returns:
            Dict with parsed cards and raw HTML
        """
        space_url = self.space_urls.get("GRAPHICS")
        if not space_url:
            raise ValueError("GRAPHICS mode HF Space URL not configured")

        space_id = space_url.replace("https://huggingface.co/spaces/", "")

        html = await asyncio.to_thread(
            self._call_graphics_inspiration,
            space_id,
            query,
        )

        items = self._parse_graphics_inspiration(html)

        return {
            "items": items,
            "raw_html": html,
        }

    def _call_graphics_inspiration(self, space_id: str, query: str) -> str:
        """Call the inspiration endpoint and return HTML."""
        client = Client(space_id, hf_token=self.hf_token)

        try:
            client.predict(api_name="/switch_to_inspiration")
        except Exception as exc:
            logger.warning("Failed to switch to inspiration mode: %s", exc)

        result = client.predict(
            query,
            api_name="/search_with_loading",
        )

        if isinstance(result, str):
            return result

        return json.dumps(result)

    def _parse_graphics_inspiration(self, html: str) -> List[Dict[str, Optional[str]]]:
        """Parse returned HTML into structured cards."""
        cards: List[Dict[str, Optional[str]]] = []

        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception as exc:
            logger.error("Failed to parse graphics inspiration HTML: %s", exc)
            return cards

        for card_div in soup.find_all("div"):
            style = card_div.get("style") or ""
            if "box-shadow" not in style:
                continue

            title_tag = card_div.find("h3")
            if not title_tag:
                continue

            paragraphs = card_div.find_all("p")
            source = paragraphs[0].get_text(strip=True) if paragraphs else None
            date = paragraphs[1].get_text(strip=True) if len(paragraphs) > 1 else None
            link_tag = card_div.find("a", href=True)
            img_tag = card_div.find("img")
            image = None
            if img_tag:
                src = (img_tag.get("src") or "").strip()
                if src and src.lower() != "nan":
                    image = src

            cards.append(
                {
                    "title": title_tag.get_text(strip=True),
                    "source": source,
                    "date": date,
                    "url": link_tag["href"] if link_tag else None,
                    "image": image,
                }
            )

        logger.info("Parsed %d inspiration cards", len(cards))
        return cards

# Global instance
hf_spaces_client = HFSpacesClient()
