# app/config.py
import os
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Cruise Bot"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # WhatsApp
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    PHONE_NUMBER_ID: str = os.getenv("PHONE_NUMBER_ID", "")
    VERIFY_TOKEN: str = os.getenv("VERIFY_TOKEN", "")
    
    # Instagram
    INSTAGRAM_TOKEN: str = os.getenv("INSTAGRAM_TOKEN", "")
    IG_BUSINESS_ID: str = os.getenv("IG_BUSINESS_ID", "")
    
    # Redis (for caching and rate limiting)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def database_url_with_ssl(self) -> str:
        """Add SSL requirement for Render PostgreSQL"""
        if "render.com" in self.DATABASE_URL and "sslmode" not in self.DATABASE_URL:
            # Add SSL mode for Render connections
            return f"{self.DATABASE_URL}?sslmode=require"
        return self.DATABASE_URL
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()