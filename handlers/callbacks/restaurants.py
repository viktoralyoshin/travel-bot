import os
from telegram import InputMediaPhoto, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.main import get_back_to_menu_button


async def restaurants_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    keyboard = [get_back_to_menu_button()]

    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_path = os.path.join("assets", "images", "restaurants.jpg")

    await query.edit_message_media(
        media=InputMediaPhoto(media=open(photo_path, "rb")), reply_markup=reply_markup
    )
