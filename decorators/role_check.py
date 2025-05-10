from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from db.db import get_db
from db.repositories.users import UserRepository
from db.models import Role

def require_role(required_role: Role):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if not update.effective_user:
                return
            
            async with get_db() as session:
                repo = UserRepository(session)
                user = await repo.get_by_telegram_id(update.effective_user.id)
                
                if not user or user.role < required_role:
                    await update.message.reply_text("⚠️ У вас недостаточно прав для выполнения этой команды.")
                    return
                
                return await handler(update, context, *args, **kwargs)
        return wrapper
    return decorator