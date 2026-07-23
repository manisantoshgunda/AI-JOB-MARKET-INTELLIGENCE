import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application Configuration
APP_NAME = os.getenv("APP_NAME", "AI Job Market Intelligence Platform")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

# Upload Configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///job_market.db")