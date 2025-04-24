import os
from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes

from keyboards.main import get_main_menu_keyboard

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    user = update.effective_user
    query = update.callback_query if is_callback else None

    photo_path = os.path.join("assets", "images", "main.jpg")

    welcome_text = (
        f"Привет, {user.first_name}! 👋\n"
        "Я — твой гид по Иркутску. Вот что я умею:\n\n"
        "📍 /attractions — Достопримечательности\n"
        "🍴 /restaurants — Кафе и рестораны\n"
        "❓ /help — Помощь"
    )

    if is_callback: 
        await update.callback_query.edit_message_media(
            media=InputMediaPhoto(media=open(photo_path, 'rb'), caption=welcome_text),
            reply_markup=get_main_menu_keyboard()
        )
    
    else:
        await update.message.reply_photo(
            photo=open(photo_path, 'rb'),
            caption=welcome_text,
            reply_markup=get_main_menu_keyboard()
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)
