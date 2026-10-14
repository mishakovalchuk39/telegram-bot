import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Вставь сюда свой токен от BotFather
TOKEN = "ВСТАВ_СВІЙ_ТОКЕН_СЮДИ"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    # add_get автоматически обрабатывает и GET, и HEAD запросы Render
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")

# --- КНОПКИ И ОБРАБОТЧИК СТАРТА ---
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
                    url="https://t.me/rubin_shoupp"  # Вкажи юзернейм менеджера
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

# Обработчик кнопки "ВІДКРИТИ КАТАЛОГ"
@dp.callback_query(lambda c: c.data == "open_catalog")
async def process_catalog(callback_query: types.CallbackQuery):
    catalog_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ВЕРХНІЙ ОДЯГ ↗️", 
                    url="https://t.me/rubin_shoupp"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ГОЛОВНІ УБОРИ ↗️", 
                    url="https://t.me/rubin_shoupp"
                )
            ]
        ]
    )
    
    await callback_query.message.answer("Привіт! Обери категорію нижче:", reply_markup=catalog_keyboard)
    await callback_query.answer()

# --- ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ---
async def main():
    await start_web_server()
    logging.info("Бот успішно запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
