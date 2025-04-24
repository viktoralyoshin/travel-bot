from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )

        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )

        return result.scalars().all()

    async def create(self, data: dict) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def update(self, id: int, data: dict) -> Optional[ModelType]:
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(**data)
        )
        await self.session.commit()

        return await self.get(id)
    
    async def delete(self, id: int) -> bool: 
        await self.session.execute(delete(self.model).where(self.nodel.id == id))
        await self.session.commit()
        
        return True
