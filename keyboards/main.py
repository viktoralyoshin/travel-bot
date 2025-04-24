from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard():

    keyboard = [
        [InlineKeyboardButton("📍Достопримечательности", callback_data="attractions")],
        [InlineKeyboardButton("🍴Кафе и рестораны", callback_data="restaurants")],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_to_menu_button():
    return [InlineKeyboardButton("👈 Назад в меню", callback_data="back_to_menu")]
