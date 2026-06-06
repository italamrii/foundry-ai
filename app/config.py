from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DB_PATH = STORAGE_DIR / "foundry.db"

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

PROJECT_TYPES = [
    "SaaS",
    "Mobile App",
    "Desktop App",
    "AI Tool",
    "Marketplace",
    "E-Commerce",
    "Game",
    "Startup",
    "Other",
]
