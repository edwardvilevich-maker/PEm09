from typing import Optional

from services.memory import memory
from services.openai_client import chat_completion
from rag.rag_service import rag_service


SYSTEM_PROMPT = (
    "Ты HR-ассистент компании. Отвечай кратко и понятно, "
    "ориентируясь на регламенты, правила, график работы, отпуска, дресс-код "
    "и внутренние контакты. Если чего-то нет в базе, отвечай общими рекомендациями."
)


async def handle_text(user_id: int, text: str) -> str:
    mode = memory.get_mode(user_id)
    memory.add_message(user_id, "user", text)

    if mode == "rag":
        answer = await _answer_with_rag(user_id, text)
    else:
        answer = await _answer_plain(user_id, text)

    memory.add_message(user_id, "assistant", answer)
    return answer


async def _answer_plain(user_id: int, text: str) -> str:
    history = memory.get_history(user_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for role, content in history:
        messages.append({"role": role, "content": content})
    return chat_completion(messages)


async def _answer_with_rag(user_id: int, text: str) -> str:
    context, metadatas = rag_service.query(text)

    history = memory.get_history(user_id)
    messages = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + " Используй следующий контекст из базы знаний. "
                "Если ответ основан на нём, обязательно укажи, из какого файла взята информация."
            ),
        },
        {"role": "system", "content": f"Контекст:\n{context}"},
    ]
    for role, content in history:
        messages.append({"role": role, "content": content})

    answer = chat_completion(messages)

    # Добавим явное упоминание источников (если они есть)
    unique_files = {m.get("filename") for m in metadatas if m.get("filename")}
    if unique_files:
        sources_str = ", ".join(sorted(unique_files))
        answer += f"\n\nИсточник(и): {sources_str}"
    return answer


async def handle_voice_text(user_id: int, recognized_text: str) -> str:
    memory.add_message(user_id, "user", f"(Голосовое сообщение) {recognized_text}")
    # Логика та же, что и для обычного текста, но мы явно упоминаем, что это было голосовое.
    return await handle_text(user_id, recognized_text)


async def handle_image_description(user_id: int, description: str) -> str:
    memory.add_message(user_id, "user", f"(Картинка) {description}")
    memory.add_message(user_id, "assistant", description)
    return description


def get_stats() -> str:
    return rag_service.stats()

