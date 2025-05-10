from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.admin_commands import admin_help, make_admin, start_create_attraction, start_create_restaurant, stats_command
from handlers.callbacks.router import button_click
from handlers.commands import start
from dotenv import load_dotenv
import os

from handlers.message_handlers.all_messages_handler import handle_all_messages
from middleware.user_middleware import user_middleware

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    app = Application.builder().token(TOKEN).build()
    
    def wrap_handler(handler):
        async def wrapped(update, context):
            return await user_middleware(update, context, handler)
        return wrapped
    
    app.add_handler(CommandHandler("start", wrap_handler(start)))
    app.add_handler(CommandHandler("add_attraction", wrap_handler(start_create_attraction)))
    app.add_handler(CommandHandler("add_restaurant", wrap_handler(start_create_restaurant)))
    app.add_handler(CommandHandler("make_admin", wrap_handler(make_admin)))
    app.add_handler(CommandHandler("stats", wrap_handler(stats_command)))
    app.add_handler(CommandHandler("admin_help", wrap_handler(admin_help)))
    
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        wrap_handler(handle_all_messages)
    ))
    
    app.add_handler(CallbackQueryHandler(wrap_handler(button_click)))

    app.run_polling()

if __name__ == "__main__":
    main()