import os
import tempfile

from aiogram import Router, types, F

from services.openai_client import vision_completion
from services.router import handle_image_description


router = Router()


@router.message(F.photo)
async def handle_photo(message: types.Message):
    # Берём фото наибольшего размера
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "image.jpg")
        await message.bot.download_file(file.file_path, destination=img_path)

        # В простом варианте шлём как data-url в Vision
        # (в реальном бою можно загрузить на свой CDN и передать URL).
        with open(img_path, "rb") as f:
            data = f.read()

        import base64

        b64 = base64.b64encode(data).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{b64}"

        description = vision_completion(data_url, "Опиши подробно, что изображено на картинке.")
        final_answer = await handle_image_description(message.from_user.id, description)

        await message.answer(final_answer)

