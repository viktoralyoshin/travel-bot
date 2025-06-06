from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Attraction


class AttractionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, sort_by_rating: bool = False):
        query = select(Attraction)
        
        if sort_by_rating:
            query = query.order_by(desc(Attraction.rating))
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, id: int):
        result = await self.session.execute(select(Attraction).where(Attraction.id == id))
        return result.scalar_one_or_none()

    async def create(
        self,
        name: str,
        description: str,
        image_url: str,
        address: str,
        rating: int,
        yandex_url: str,
    ):
        attraction = Attraction(
            name=name,
            description=description,
            image_url=image_url,
            address=address,
            rating=rating,
            yandex_url=yandex_url,
        )

        self.session.add(attraction)
        await self.session.commit()

        return attraction