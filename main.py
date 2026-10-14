import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

TOKEN = "8909701110:AAHrmwTlZHxS9zfXMD3KbBf01_yuaurX94"

router = Router()

catalog_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="ВЕРХНІЙ ОДЯГ",
                url="https://t.me/outerwear32"
            )
        ],
        [
            InlineKeyboardButton(
                text="ГОЛОВНІ УБОРИ",
                url="https://t.me/rubin_shoupp"
            )
        ]
    ]
)


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Привіт! Обери каталог:", reply_markup=catalog_keyboard)


# Веб-сервер для Render (порт 10000)
async def handle(request):
    return web.Response(text="Bot is running!")


async def main():
    logging.basicConfig(level=logging.INFO)

    # Запуск веб-сервера aiohttp
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот успішно запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())