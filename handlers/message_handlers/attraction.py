from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from db.db import get_db
from db.models import Attraction
from db.repositories.attractions import AttractionRepository


async def handle_attraction_creation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not context.user_data.get("creating_attraction"):
        return

    try:
        step = context.user_data["creating_attraction"]["step"]
        user_data = context.user_data["creating_attraction"]

        if step == 1:
            user_data["name"] = update.message.text
            user_data["step"] = 2
            await update.message.reply_text("Введите описание:")

        elif step == 2:
            user_data["description"] = update.message.text
            user_data["step"] = 3
            await update.message.reply_text("Введите ссылку на картинку:")

        elif step == 3:
            user_data["image_url"] = update.message.text
            user_data["step"] = 4
            await update.message.reply_text("Адрес:")

        elif step == 4:
            user_data["address"] = update.message.text
            user_data["step"] = 5
            await update.message.reply_text(
                "Введите число от 1 до 5",
            )

        elif step == 5:
            try:
                rating = float(update.message.text)
                if not 1 <= rating <= 5:
                    raise ValueError

                user_data["rating"] = rating
                user_data["step"] = 6
                await update.message.reply_text(
                    "Введите Yandex URL (или отправьте '-' чтобы пропустить):",
                )

            except ValueError:
                await update.message.reply_text(
                    "Неверный рейтинг. Введите число от 1 до 5"
                )

        elif step == 6:
            yandex_url = update.message.text if update.message.text != "-" else ""

            async with get_db() as session:
                repo = AttractionRepository(session)
                await repo.create(
                    name=user_data["name"],
                    description=user_data["description"],
                    image_url=user_data["image_url"],
                    address=user_data["address"],
                    rating=user_data["rating"],
                    yandex_url=yandex_url,
                )

            await update.message.reply_text(
                "✅ Достропримечательность успешно создана!",
            )
            context.user_data.pop("creating_attraction", None)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "❌ Произошла ошибка при создании",
        )
        context.user_data.pop("creating_attraction", None)
