from telegram import Update
from telegram.ext import ContextTypes

from handlers.commands import show_main_menu

async def back_to_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_main_menu(update, context, is_callback=True)