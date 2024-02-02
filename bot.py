import asyncio
import logging
import subprocess
import os

from datetime import datetime
from model import predict

from aiogram import filters, html
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters import command, CommandObject, CommandStart
from aiogram.utils.formatting import (
    Bold,
    as_list,
    as_marked_section,
    as_key_value,
    HashTag,
)
from config_reader import config
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

START_MESSAGE = """
Hello, it's auto model detection model.
Send me photo and i try to detect what model is!
"""

INFO_MESSAGE = """
I'm bot using Yolov8 model
I trained on 8k photos
Training and validating size: 6506 and 1626
"""

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE)

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(INFO_MESSAGE)

@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    os.makedirs("/temp_folder/telegram_photos/", exist_ok=True)
    await bot.download(
        message.photo[-1],
        destination=f"/temp_folder/telegram_photos/predict_{message.message_id}.jpg",
    )
    file_ids = []

    print("Predicted started")
    await predict()
    print("Predicted stopped")

    image_from_pc = FSInputFile("runs/detect/predict/predict.jpg")
    await message.answer_photo(image_from_pc, caption="")
    subprocess.run("rm -rf runs/detect/predict/".split(" "))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
