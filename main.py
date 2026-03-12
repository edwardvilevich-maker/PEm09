import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from utils.config import settings
from handlers.commands import router as commands_router
from handlers.text_handler import router as text_router
from handlers.voice_handler import router as voice_router
from handlers.image_handler import router as image_router
from rag.rag_service import rag_service


async def main() -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    # Индексация базы знаний при старте
    rag_service.ingest_data_dir()

    bot = Bot(token=settings.telegram_bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(commands_router)
    dp.include_router(voice_router)
    dp.include_router(image_router)
    dp.include_router(text_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

