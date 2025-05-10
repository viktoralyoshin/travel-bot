from telegram import Update
from telegram.ext import ContextTypes

from handlers.callbacks.attraction_id import attraction_detail_callback
from handlers.callbacks.attractions import attractions_callback
from handlers.callbacks.menu import back_to_menu_callback
from handlers.callbacks.restaurant_id import restaurant_detail_callback
from handlers.callbacks.restaurants import restaurants_callback
from handlers.commands import show_main_menu

callback_handlers = {
    "attractions": attractions_callback,
    "restaurants": restaurants_callback,
    "back_to_menu": back_to_menu_callback,
}


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("attraction_"):
        await attraction_detail_callback(update, context)
    elif query.data.startswith("restaurant_"):
        await restaurant_detail_callback(update, context)
    elif query.data.startswith("restaurants_page_"):
        # Обработка пагинации для ресторанов
        page = int(query.data.split("_")[-1])
        context.args = [str(page)]  # Передаем номер страницы как аргумент
        await restaurants_callback(update, context)
    elif query.data.startswith("attractions_page_"):
        # Аналогично можно добавить пагинацию для достопримечательностей
        page = int(query.data.split("_")[-1])
        context.args = [str(page)]
        await attractions_callback(update, context)
    else:
        handler = callback_handlers.get(query.data)
        if handler:
            await handler(update, context)
        else:
            await show_main_menu(update, context, is_callback=True)