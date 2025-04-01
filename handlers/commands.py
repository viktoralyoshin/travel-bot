from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    welcome_text = (
        f"Привет, {user.first_name}! 👋\n"
        "Я — твой гид по Иркутску. Вот что я умею:\n\n"
        "📍 /attractions — Достопримечательности\n"
        "🍴 /restaurants — Кафе и рестораны\n"
        "❓ /help — Помощь"
    )

    keybord = [
        [InlineKeyboardButton("📍Достопримечательности", callback_data="attractions")],
        [InlineKeyboardButton("🍴Кафе и рестораны", callback_data="restaurants")],
        [InlineKeyboardButton("❓Помощь", callback_data="help")],
    ]

    reply_markup = InlineKeyboardMarkup(keybord)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = (
        "Список команд:\n"
        "/start — Начало работы\n"
        "/attractions — Куда сходить\n"
        "/restaurants — Где поесть"
    )

    await update.message.reply_text(help_text)
