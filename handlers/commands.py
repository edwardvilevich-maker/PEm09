from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from services.memory import memory
from services.router import get_stats


router = Router()


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/mode rag"),
                KeyboardButton(text="/mode text"),
            ],
            [
                KeyboardButton(text="/mode voice"),
                KeyboardButton(text="/reset"),
            ],
            [
                KeyboardButton(text="/stats"),
                KeyboardButton(text="/help"),
            ],
        ],
        resize_keyboard=True,
    )


WELCOME_TEXT = (
    "Привет! Я HR-ассистент для новичков компании.\n\n"
    "Я могу рассказать о графике работы, отпусках, корпоративных правилах, "
    "дресс-коде и контактах отделов. "
    "Также я умею работать в режимах текст/RAG/voice и анализировать картинки.\n\n"
    "Доступные команды:\n"
    "/start — начать работу\n"
    "/help — краткая справка\n"
    "/reset — очистить историю диалога\n"
    "/stats — статус базы знаний\n"
    "/mode rag — включить режим RAG\n"
    "/mode text — обычный текстовый режим\n"
    "/mode voice — голосовой режим (ожидание голосовых сообщений)"
)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_keyboard())


@router.message(Command("reset"))
async def cmd_reset(message: types.Message):
    user_id = message.from_user.id
    memory.reset(user_id)
    await message.answer("История диалога очищена. Режим возвращён в text.", reply_markup=main_keyboard())


@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    stats = get_stats()
    await message.answer(stats)


@router.message(Command("mode"))
async def cmd_mode(message: types.Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer(
            "Использование: /mode rag | /mode text | /mode voice\n"
            "Для работы с базой знаний выберите режим /mode rag.",
            reply_markup=main_keyboard(),
        )
        return

    mode = parts[1].strip().lower()
    if mode not in {"rag", "text", "voice"}:
        await message.answer(
            "Неизвестный режим. Доступные: rag, text, voice.",
            reply_markup=main_keyboard(),
        )
        return

    memory.set_mode(user_id, mode)  # type: ignore[arg-type]

    if mode == "rag":
        text = "Режим RAG включён. Вопросы будут отвечаться с учётом базы знаний."
    elif mode == "voice":
        text = "Режим voice включён. Отправьте голосовое сообщение (5–10 секунд)."
    else:
        text = "Режим text включён. Ответы идут напрямую от модели без RAG."

    await message.answer(text, reply_markup=main_keyboard())

