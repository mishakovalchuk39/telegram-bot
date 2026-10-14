import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Встав сюди свій токен бота від BotFather
TOKEN = "8909701110:AAFPzpyYm1X3PIHk1a5NEv992Kcm_9qd5G0"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Bot is running!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")


# --- ГОЛОВНЕ МЕНЮ ТА КОМАНДА /start ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📁 ВІДКРИТИ КАТАЛОГ",
                    callback_data="open_catalog"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 ЗВ'ЯЗОК З МЕНЕДЖЕРОМ",
                    url="https://t.me/Mikhail34211"
                )
            ]
        ]
    )

    text = (
        "Привіт! 👋\n"
        "Ласкаво просимо до нашого магазину.\n"
        "Обери потрібну категорію нижче:"
    )

    await message.answer(text, reply_markup=keyboard)


# --- ОБРОБНИК КНОПКИ "ВІДКРИТИ КАТАЛОГ" ---
@dp.callback_query(lambda c: c.data == "open_catalog")
async def process_catalog(callback_query: types.CallbackQuery):
    catalog_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ВЕРХНІЙ ОДЯГ ↗️",
                    url="https://t.me/outerwear32"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ВЗУТТЯ ↗️",
                    url="https://t.me/shoes323"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ГОЛОВНІ УБОРИ ↗️",
                    url="https://t.me/headwear32"
                )
            ],
            [
                InlineKeyboardButton(
                    text="СУМКИ ТА АКСЕСУАРИ ↗️",
                    url="https://t.me/drop_accessories1"
                )
            ]
        ]
    )

    await callback_query.message.answer("Привіт! Обери категорію нижче:", reply_markup=catalog_keyboard)
    await callback_query.answer()


# --- ГОЛОВНА ФУНКЦІЯ ЗАПУСКУ ---
async def main():
    await start_web_server()
    # Прибираємо старий вебхук, щоб поллінг запрацював на 100%
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот успішно запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
