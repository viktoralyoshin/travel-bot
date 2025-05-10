from telegram import Update
from telegram.ext import ContextTypes
from db.db import get_db
from db.models import Role
from db.repositories.users import UserRepository


async def user_middleware(
    update: Update, context: ContextTypes.DEFAULT_TYPE, next_handler
):
    if not update.effective_user:
        return await next_handler(update, context)

    action = None
    if update.message and update.message.text:
        action = f"message:{update.message.text[:50]}"
    elif update.callback_query:
        action = f"callback:{update.callback_query.data}"

    async with get_db() as session:
        repo = UserRepository(session)
        user = await repo.get_or_create(
            telegram_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
        )

        if action:
            await repo.log_activity(telegram_id=update.effective_user.id, action=action)

        context.user_data["db_user"] = user
        context.user_data["user_role"] = user.role

    return await next_handler(update, context)
