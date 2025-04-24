import os
from telegram import InlineKeyboardButton, InputMediaPhoto, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.db import get_db
from db.repositories.attractions import AttractionRepository
from keyboards.main import get_back_to_menu_button


async def attractions_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    photo_path = os.path.join("assets", "images", "attractions.webp")

    try:
        async with get_db() as session:
            repo = AttractionRepository(session)
            attractions = await repo.get_all()

            if not attractions:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=open(photo_path, "rb"),
                        caption="😔 Пока нет доступных достопримечательностей",
                    ),
                    reply_markup=InlineKeyboardMarkup([get_back_to_menu_button()]),
                )
                return

            text = "🏛️ Выберите достопримечательность:\n\n" + "\n".join(
                f"{idx+1}. {attr.name}" for idx, attr in enumerate(attractions)
            )

            attractions_buttons = [
                [InlineKeyboardButton(attr.name, callback_data=f"attraction_{attr.id}")]
                for attr in attractions
            ]

            keyboard = attractions_buttons + [get_back_to_menu_button()]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_media(
                media=InputMediaPhoto(media=open(photo_path, "rb"), caption=text),
                reply_markup=reply_markup,
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
