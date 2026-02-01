import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("alisa")

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIDEO_FILE_ID = os.getenv("VIDEO_FILE_ID")  # сюда потом вставим
VIDEO_URL = os.getenv("VIDEO_URL")          # запасной вариант, можно не трогать

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN environment variable")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def on_start(message: Message):
    # /start -> сразу видео
    if VIDEO_FILE_ID:
        await bot.send_video(chat_id=message.chat.id, video=VIDEO_FILE_ID)
        return

    if VIDEO_URL:
        await bot.send_video(chat_id=message.chat.id, video=VIDEO_URL)
        return

    await message.answer(
        "Видео ещё не настроено.\n"
        "Отправь мне mp4 сюда в чат — я выведу VIDEO_FILE_ID в логах.\n"
        "Потом вставишь его в Railway Variables."
    )


@dp.message(F.video)
async def capture_video_id(message: Message):
    # когда ты отправишь видео — печатаем file_id в логи
    file_id = message.video.file_id
    log.info(f"VIDEO_FILE_ID (copy this): {file_id}")
    await message.answer("Ок ✅ Я вывел VIDEO_FILE_ID в логах. Скопируй и вставь в Railway Variables.")


@dp.message()
async def fallback(message: Message):
    await message.answer("Нажми /start 🙂")


async def main():
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())
