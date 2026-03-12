import os
import tempfile

from aiogram import Router, types, F
from aiogram.types import FSInputFile

from services.memory import memory
from services.openai_client import speech_to_text, text_to_speech
from services.router import handle_voice_text


router = Router()


@router.message(F.voice)
async def handle_voice(message: types.Message):
    user_id = message.from_user.id
    mode = memory.get_mode(user_id)

    if mode != "voice":
        await message.answer("Сейчас голосовой режим выключен. Включите его командой /mode voice.")
        return

    voice = message.voice
    file = await message.bot.get_file(voice.file_id)

    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_path = os.path.join(tmpdir, "input.ogg")
        await message.bot.download_file(file.file_path, destination=ogg_path)

        recognized_text = speech_to_text(ogg_path)
        text_reply = await handle_voice_text(user_id, recognized_text)

        tts_path = os.path.join(tmpdir, "reply.mp3")
        text_to_speech(text_reply, tts_path)

        await message.answer(f"Отправил голосовое: {recognized_text}")
        voice_input = FSInputFile(tts_path)
        await message.answer_voice(voice_input, caption="Мой ответ в аудио-формате.")

