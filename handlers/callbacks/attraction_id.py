import os
from telegram import Update, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.db import get_db
from db.repositories.attractions import AttractionRepository
from keyboards.main import get_back_to_menu_button


async def attraction_detail_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    photo_path = os.path.join("assets", "images", "attractions.webp")

    try:
        attraction_id = int(query.data.split("_")[1])
        print(attraction_id)

        async with get_db() as session:
            repo = AttractionRepository(session)
            attraction = await repo.get_by_id(attraction_id)

            if not attraction:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=open(photo_path, "rb"),
                        caption="🚫 Достопримечательность не найдена",
                    ),
                    reply_markup=InlineKeyboardMarkup([get_back_to_menu_button()]),
                )
                return

            text = (
                f"🏛 <b>{attraction.name}</b>\n\n"
                f"📝 {attraction.description}\n\n"
                f"📍 Адрес: {attraction.address}\n"
                f"⭐ Рейтинг: {attraction.rating}/5\n"
            )

            keyboard = []

            if attraction.yandex_url:
                text += f"\n🌐 <a href='{attraction.yandex_url}'>Яндекс.Карты</a>"
                keyboard = [
                    [InlineKeyboardButton("📍 На карте", url=attraction.yandex_url)]
                ]

            # keyboard = []
            # if attraction.yandex_url:
            #     keyboard.append(
            #         [InlineKeyboardButton("📍 На карте", url=attraction.yandex_url)]
            #     )
            # keyboard.append([get_back_to_menu_button()])

            keyboard += [get_back_to_menu_button()]

            await query.edit_message_media(
                media=InputMediaPhoto(
                    media=attraction.image_url, caption=text, parse_mode="HTML"
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
