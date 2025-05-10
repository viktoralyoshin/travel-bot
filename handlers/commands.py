import os
from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes

from keyboards.main import get_main_menu_keyboard

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    user = update.effective_user
    query = update.callback_query if is_callback else None

    photo_path = os.path.join("assets", "images", "main.jpg")

    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я — TravelBot Irkutsk, твой помощник в путешествии по Иркутску!\n\n"
        "✨ <b>Что я могу рассказать:</b>\n\n"
        "- 🏛️ Достопримечательности — топ мест с фото и описанием\n"
        "- 🍽️ Кафе и рестораны — уютные кафе и рестораны\n\n"
        "Выбирай категорию ниже!"
    )

    if is_callback: 
        await update.callback_query.edit_message_media(
            media=InputMediaPhoto(media=open(photo_path, 'rb'), caption=welcome_text, parse_mode='HTML'),
            reply_markup=get_main_menu_keyboard()
        )
    
    else:
        await update.message.reply_photo(
            photo=open(photo_path, 'rb'),
            caption=welcome_text,
            parse_mode='HTML',
            reply_markup=get_main_menu_keyboard()
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)