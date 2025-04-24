from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from db.init_db import init_models
from db.session import get_db
from handlers.callbacks.router import button_click
from handlers.commands import start
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def main():

    await init_models()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(button_click))

    app.bot_data["get_db"] = get_db

    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

        print("Бот успешно запущен!")

        while True:
            await asyncio.sleep(3600)

        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
    except Exception as e:
        print(f"Ошибка: {e}")
