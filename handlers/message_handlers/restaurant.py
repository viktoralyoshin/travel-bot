from telegram import Update
from telegram.ext import ContextTypes

from db.db import get_db
from db.repositories.restaurants import RestaurantRepository


async def handle_restaurant_creation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    
    if not context.user_data.get("creating_restaurant"):
        return

    try:
        step = context.user_data["creating_restaurant"]["step"]
        user_data = context.user_data["creating_restaurant"]

        if step == 1:
            user_data["name"] = update.message.text
            user_data["step"] = 2
            await update.message.reply_text("Введите описание")

        elif step == 2:
            user_data["description"] = update.message.text
            user_data["step"] = 3
            await update.message.reply_text("Отправьте ссылку на картинку")

        elif step == 3:
            user_data["image_url"] = update.message.text
            user_data["step"] = 4
            await update.message.reply_text("Введите адрес")

        elif step == 4:
            user_data["address"] = update.message.text
            user_data["step"] = 5
            await update.message.reply_text("Введите средний чек")

        elif step == 5:
            average_price = int(update.message.text)
            user_data["average_price"] = average_price
            user_data["step"] = 6
            await update.message.reply_text("Введите рейтинг (число от 1 до 5)")

        elif step == 6:
            try:
                rating = float(update.message.text)
                if not 1 <= rating <= 5:
                    raise ValueError

                user_data["rating"] = rating
                user_data["step"] = 7
                await update.message.reply_text(
                    "Введите Yandex URL (или отправьте '-' чтобы пропустить)",
                )

            except ValueError:
                await update.message.reply_text(
                    "Неверный рейтинг. Введите число от 1 до 5"
                )

        elif step == 7:
            yandex_url = update.message.text if update.message.text != "-" else ""

            async with get_db() as session:
                repo = RestaurantRepository(session)
                await repo.create(
                    name=user_data["name"],
                    description=user_data["description"],
                    image_url=user_data["image_url"],
                    address=user_data["address"],
                    average_price=user_data["average_price"],
                    rating=user_data["rating"],
                    yandex_url=yandex_url,
                )

            await update.message.reply_text(
                "✅ Ресторан успешно создан!",
            )
            context.user_data.pop("creating_restaurant", None)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "❌ Произошла ошибка при создании",
        )
        context.user_data.pop("creating_restaurant", None)
