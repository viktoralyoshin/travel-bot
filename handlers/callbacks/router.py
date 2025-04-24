from telegram import Update
from telegram.ext import ContextTypes

from handlers.callbacks.attractions import attractions_callback
from handlers.callbacks.menu import back_to_menu_callback
from handlers.callbacks.restaurants import restaurants_callback
from handlers.commands import show_main_menu

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_handlers = {
        "attractions": attractions_callback,
        "restaurants": restaurants_callback,
        "back_to_menu": back_to_menu_callback
    }

    handler = callback_handlers.get(query.data)
    if handler:
        await handler(update, context)
    else:
        await show_main_menu(update, context, is_callback=True)