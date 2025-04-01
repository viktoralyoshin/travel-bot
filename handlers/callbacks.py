from telegram import Update
from telegram.ext import ContextTypes

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "attractions":
        await query.edit_message_text("Вот список достопримечательностей: /attractions")
    elif query.data == "restaurants":
        await query.edit_message_text("Вот список ресторанов: /restaurants")
    elif query.data == "help":
        await query.edit_message_text("Помощь: /help")