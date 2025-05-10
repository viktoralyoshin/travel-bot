from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from db.db import get_db
from db.models import Role
from db.repositories.users import UserRepository
from decorators.role_check import require_role


@require_role(Role.ADMIN)
async def start_create_attraction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["creating_attraction"] = {"step": 1}
    await update.message.reply_text("Введите название достопримечательности")


@require_role(Role.ADMIN)
async def start_create_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["creating_restaurant"] = {"step": 1}
    await update.message.reply_text("Введите название ресторана или кафе")


@require_role(Role.ADMIN)
async def make_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Укажите ID пользователя: /make_admin <user_id>"
        )
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Некорректный ID пользователя")
        return

    async with get_db() as session:
        repo = UserRepository(session)
        target_user = await repo.get_by_telegram_id(target_id)
        if not target_user:
            await update.message.reply_text("Пользователь не найден")
            return

        updated_user = await repo.update_role(target_id, Role.ADMIN)

        if updated_user:
            await update.message.reply_text(
                f"✅ Пользователь @{updated_user.username or updated_user.first_name} "
                f"(ID: {updated_user.telegram_id}) теперь администратор!"
            )
        else:
            await update.message.reply_text("Не удалось обновить роль пользователя")


@require_role(Role.ADMIN)
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with get_db() as session:
        repo = UserRepository(session)

        total_users = await repo.get_user_count()
        active_users = await repo.get_active_users_count()
        new_users = await repo.get_new_users_count()
        users_by_roles = await repo.get_users_by_roles()

        roles_stats = "\n".join(
            f"• {Role(role).value}: {count}" for role, count in users_by_roles.items()
        )

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = (
            f"📊 <b>Статистика бота</b> (на {current_date})\n\n"
            f"👥 <b>Всего пользователей:</b> {total_users}\n"
            f"🟢 <b>Активных (7 дней):</b> {active_users}\n"
            f"🆕 <b>Новых (7 дней):</b> {new_users}\n\n"
            f"👑 <b>Распределение по ролям:</b>\n{roles_stats}"
        )

        await update.message.reply_html(message)


@require_role(Role.ADMIN)
async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🛠️ <b>Админ-команды</b>:

• <code>/make_admin [user_id]</code> - Назначить пользователя администратором
• <code>/stats</code> - Показать статистику бота
• <code>/add_attraction</code> - Добавить новую достопримечательность
• <code>/add_restaurant</code> - Добавить новый ресторан
"""
    await update.message.reply_html(help_text)
