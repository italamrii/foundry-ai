from app.config import STORAGE_DIR
from data.database import init_db


def bootstrap_app() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    init_db()
