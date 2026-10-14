import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

# 1. ТВІЙ ТОКЕН
TOKEN = "8909701110:AAHrmwTlzHXs9zfXMD3KbBfVO1_yuaurX94"

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
                url="https://t.me/headwear32"  # 👈 Сюди посилання на канал
            )
        ],
        [
            InlineKeyboardButton(
                text="ВЗУТТЯ",
                url="https://t.me/shoes323"  # 👈 Сюди посилання на канал
            )
        ],
        [
            InlineKeyboardButton(
                text="СУМКИ ТА АКСЕСУАРИ",
                url="https://t.me/drop_accessories1"  # 👈 Сюди посилання на канал
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ НАЗАД",
                callback_data="back_to_main"
            )
        ],
    ]
)

# ГОЛОВНЕ МЕНЮ
main_keyboard = InlineKeyboardMarkup(
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


# Команда /start
@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привіт! 👋\n"
        "Ласкаво просимо до нашого магазину.\n"
        "Обери потрібну категорію нижче:",
        reply_markup=main_keyboard,
    )


# Відкрити каталог
@router.callback_query(F.data == "open_catalog")
async def show_catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        "Обери категорію товарів:",
        reply_markup=catalog_keyboard
    )
    await callback.answer()


# Повернутися в головне меню
@router.callback_query(F.data == "back_to_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Головне меню. Натисни кнопку нижче:",
        reply_markup=main_keyboard
    )
    await callback.answer()


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот успішно запущено!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())