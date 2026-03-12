import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    data_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    rag_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag")
    chroma_dir: str = os.path.join(rag_dir, "chroma_db")


settings = Settings()

if not settings.openai_api_key or not settings.telegram_bot_token:
    # Не выбрасываем исключение, чтобы можно было запускать части кода без ключей,
    # но явно подсвечиваем проблему в логах.
    print("WARNING: OPENAI_API_KEY or TELEGRAM_BOT_TOKEN is not set in .env")
