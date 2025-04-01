from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers.callbacks import button_click
from handlers.commands import start, help
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))

    app.add_handler(CallbackQueryHandler(button_click))

    app.run_polling()


if __name__ == "__main__":
    main()
