from aiogram import Router, types
from aiogram.filters import Command

from services.memory import memory
from services.router import handle_text


router = Router()


@router.message()
async def handle_any_text(message: types.Message):
    # Игнорируем команды здесь, они обрабатываются в commands.py
    if message.text and message.text.startswith("/"):
        return

    user_id = message.from_user.id
    mode = memory.get_mode(user_id)

    reply_prefix = ""
    if mode == "rag":
        reply_prefix = "[RAG] "
    elif mode == "voice":
        reply_prefix = "[voice/text] "

    answer = await handle_text(user_id, message.text or "")
    await message.answer(f"{reply_prefix}{answer}")

