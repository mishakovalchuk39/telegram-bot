import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

# 1. ТВОЙ ТОКЕН
TOKEN = "8909701110:AAHrmwTlzHXs9zfXMD3KbBf01_yuaurX94"

router = Router()

# КНОПКИ КАТАЛОГУ (ВІДРАЗУ ВЕДУТЬ НА КАНАЛИ)
catalog_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="ВЕРХНІЙ ОДЯГ",
                url="https://t.me/outerwear32"  # 👈 Сюди посилання на канал
            )
        ],
        [
            InlineKeyboardButton(
                text="ГОЛОВНІ УБОРИ",
                url="https://t.me/rubin_shoupp"  # 👈 Сюди посилання на канал
            )
        ]
    ]
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привіт! Обери категорію нижче:",
        reply_markup=catalog_keyboard
    )


# Веб-сервер для того, щоб Render бачив відкритий порт 10000
async def handle(request):
    return web.Response(text="Bot is alive!")


async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()


async def main():
    # Запускаємо веб-сервер для Render перед запуском бота
    await web_server()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот успішно запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())