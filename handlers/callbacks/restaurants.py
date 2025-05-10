import os
from telegram import InlineKeyboardButton, InputMediaPhoto, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.db import get_db
from db.repositories.restaurants import RestaurantRepository
from keyboards.main import get_back_to_menu_button

# Константы для пагинации
RESTAURANTS_PER_PAGE = 5  # Количество ресторанов на одной странице


async def restaurants_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем номер страницы из callback_data (если есть)
    page = (
        int(context.args[0])
        if (hasattr(context, "args") and context.args and context.args[0].isdigit())
        else 0
    )

    photo_path = os.path.join("assets", "images", "restaurants.jpg")

    try:
        async with get_db() as session:
            repo = RestaurantRepository(session)
            all_restaurants = await repo.get_all(sort_by_rating=True)

            if not all_restaurants:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=open(photo_path, "rb"),
                        caption="😔 Пока нет доступных кафе и ресторанов",
                    ),
                    reply_markup=InlineKeyboardMarkup([get_back_to_menu_button()]),
                )
                return

            # Разбиваем на страницы
            total_pages = (
                len(all_restaurants) + RESTAURANTS_PER_PAGE - 1
            ) // RESTAURANTS_PER_PAGE
            current_page = min(
                page, total_pages - 1
            )  # Ограничиваем максимальную страницу
            start_idx = current_page * RESTAURANTS_PER_PAGE
            end_idx = start_idx + RESTAURANTS_PER_PAGE
            restaurants = all_restaurants[start_idx:end_idx]

            text = (
                f"🏛️ Выберите кафе или ресторан (Страница {current_page + 1}/{total_pages}):\n\n"
                + "\n".join(
                    f"{idx+1+start_idx}. {rest.name}"
                    for idx, rest in enumerate(restaurants)
                )
            )

            # Формируем кнопки для ресторанов
            restaurants_buttons = [
                [
                    InlineKeyboardButton(
                        f"{rest.name} {rest.rating}⭐",
                        callback_data=f"restaurant_{rest.id}",
                    )
                ]
                for rest in restaurants
            ]

            # Формируем кнопки пагинации (если нужно)
            pagination_buttons = []
            if total_pages > 1:
                row = []
                if current_page > 0:
                    row.append(
                        InlineKeyboardButton(
                            "⬅️ Назад",
                            callback_data=f"restaurants_page_{current_page - 1}",
                        )
                    )
                if current_page < total_pages - 1:
                    row.append(
                        InlineKeyboardButton(
                            "Вперед ➡️",
                            callback_data=f"restaurants_page_{current_page + 1}",
                        )
                    )
                if row:
                    pagination_buttons.append(row)

            # Собираем всю клавиатуру
            keyboard = (
                restaurants_buttons + pagination_buttons + [get_back_to_menu_button()]
            )

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_media(
                media=InputMediaPhoto(media=open(photo_path, "rb"), caption=text),
                reply_markup=reply_markup,
            )

    except Exception as e:
        print(f"Error in restaurants_callback: {e}")
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=open(photo_path, "rb"),
                caption="⚠️ Произошла ошибка при загрузке данных",
            ),
            reply_markup=InlineKeyboardMarkup([[get_back_to_menu_button()]]),
        )
