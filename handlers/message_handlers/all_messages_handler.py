from telegram import Update
from telegram.ext import ContextTypes
from handlers.message_handlers.attraction import handle_attraction_creation
from handlers.message_handlers.restaurant import handle_restaurant_creation


async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("creating_restaurant"):
        await handle_restaurant_creation(update, context)
    elif context.user_data.get("creating_attraction"):
        await handle_attraction_creation(update, context)