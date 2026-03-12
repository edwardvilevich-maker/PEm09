from typing import List, Literal

from openai import OpenAI

from utils.config import settings


client = OpenAI(api_key=settings.openai_api_key)


def chat_completion(messages: List[dict], model: str = "gpt-4.1-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content or ""


def vision_completion(image_url: str, prompt: str = "Опиши, что изображено на картинке.") -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    )
    return response.choices[0].message.content or ""


def speech_to_text(audio_path: str, language: str = "ru") -> str:
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f,
            language=language,
        )
    return transcript.text


def text_to_speech(
    text: str,
    output_path: str,
    voice: Literal["alloy", "verse"] = "alloy",
) -> str:
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
    ) as response:
        response.stream_to_file(output_path)
    return output_path
