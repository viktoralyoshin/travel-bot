from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.callbacks.router import button_click
from handlers.commands import start, start_create_attraction
from dotenv import load_dotenv
import os

from handlers.message_handlers.attraction import handle_attraction_creation

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_attraction", start_create_attraction))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_attraction_creation))

    app.add_handler(CallbackQueryHandler(button_click))

    app.run_polling()

if __name__ == "__main__":
    main()