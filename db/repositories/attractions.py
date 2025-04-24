from typing import List
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Attraction
from db.repositories.base import BaseRepository

class AttractionRepository(BaseRepository[Attraction]):
    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Attraction))
        return result.scalars().all()

    async def get_top_rated(self, limit: int = 5) -> List[Attraction]:
        result = await self.session.execute(select(Attraction).order_by(desc(Attraction.rating)).limit(limit))

        return result.scalars().all()