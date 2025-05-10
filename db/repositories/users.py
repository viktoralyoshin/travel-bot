from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User, Role, UserActivity
from typing import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, telegram_id: int, username: str = None, 
                      first_name: str = None, last_name: str = None) -> User:
        user = await self.get_by_telegram_id(telegram_id)
    
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                role=Role.USER
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def update_role(self, telegram_id: int, role: Role) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.role = role
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def log_activity(self, telegram_id: int, action: str, details: str = None):
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.last_activity = datetime.utcnow()
            
            activity = UserActivity(
                user_id=user.id,
                action=action,
                details=details
            )
            self.session.add(activity)
            await self.session.commit()
    
    async def get_user_count(self):
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar_one()

    async def get_active_users_count(self, days=7):
        time_threshold = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(
            select(func.count(User.id)).where(
                User.last_activity >= time_threshold
            )
        )
        return result.scalar_one()

    async def get_new_users_count(self, days=7):
        time_threshold = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(
            select(func.count(User.id)).where(
                User.created_at >= time_threshold
            )
        )
        return result.scalar_one()

    async def get_users_by_roles(self):
        result = await self.session.execute(
            select(User.role, func.count(User.id)).group_by(User.role))
        return dict(result.all())