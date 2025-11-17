"""
Application configuration using environment variables.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "Infoviz API"
    debug: bool = False
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Hugging Face
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")

    # HF Space URLs
    hf_spaces: dict = {
        "GRAPHICS": "https://huggingface.co/spaces/tomvaillant/graphics-llm",
    }

    # CORS
    allowed_origins: list[str] = [
        "http://localhost:5173",  # SvelteKit dev
        "http://localhost:7860",  # HF Spaces
        "https://*.hf.space",     # HF Spaces wildcard
        "https://infoviz.onrender.com",  # Production
        "https://*.onrender.com",  # Render.com wildcard
    ]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
