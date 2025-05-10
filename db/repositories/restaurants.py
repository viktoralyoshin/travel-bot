from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Restaurant


class RestaurantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, sort_by_rating: bool = False):
        query = select(Restaurant)
        
        if sort_by_rating:
            query = query.order_by(desc(Restaurant.rating))
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, id: int):
        result = await self.session.execute(select(Restaurant).where(Restaurant.id == id))
        return result.scalar_one_or_none()

    async def create(
        self,
        name: str,
        description: str,
        image_url: str,
        address: str,
        rating: int,
        yandex_url: str,
        average_price: int
    ):
        restaurant = Restaurant(
            name=name,
            description=description,
            image_url=image_url,
            address=address,
            rating=rating,
            yandex_url=yandex_url,
            average_price=average_price,
        )

        self.session.add(restaurant)
        await self.session.commit()

        return restaurant