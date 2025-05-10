import os
from telegram import Update, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.db import get_db
from db.repositories.restaurants import RestaurantRepository
from keyboards.main import get_back_to_menu_button


async def restaurant_detail_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    photo_path = os.path.join("assets", "images", "restaurants.jpg")

    try:
        restaurant_id = int(query.data.split("_")[1])

        async with get_db() as session:
            repo = RestaurantRepository(session)
            restaurant = await repo.get_by_id(restaurant_id)

            if not restaurant:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=open(photo_path, "rb"),
                        caption="🚫 Ресторан не найден",
                    ),
                    reply_markup=InlineKeyboardMarkup([get_back_to_menu_button()]),
                )
                return

            text = (
                f"🏛 <b>{restaurant.name}</b>\n\n"
                f"📝 {restaurant.description}\n\n"
                f"📍 Адрес: {restaurant.address}\n"
                f"⭐ Рейтинг: {restaurant.rating}\n"
                f"💵 Средний чек: {restaurant.average_price} ₽\n"
            )

            keyboard = []

            if restaurant.yandex_url:
                text += f"\n🌐 <a href='{restaurant.yandex_url}'>Яндекс.Карты</a>"
                keyboard = [
                    [InlineKeyboardButton("📍 На карте", url=restaurant.yandex_url)]
                ]

            keyboard += [get_back_to_menu_button()]

            await query.edit_message_media(
                media=InputMediaPhoto(
                    media=restaurant.image_url, caption=text, parse_mode="HTML"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    except Exception as e:
        print(e)
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=open(photo_path, "rb"),
                caption="⚠️ Произошла ошибка при загрузке данных",
            ),
            reply_markup=InlineKeyboardMarkup([get_back_to_menu_button()]),
        )
