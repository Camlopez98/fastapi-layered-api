"""
Repositorio de Categoria (patron Repository asincrono).
"""

from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        return await self._session.get(Category, category_id)

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self._session.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()

    async def list(self, *, offset: int = 0, limit: int = 20) -> tuple[Sequence[Category], int]:
        items_result = await self._session.execute(
            select(Category).order_by(Category.id).offset(offset).limit(limit)
        )
        total_result = await self._session.execute(select(func.count()).select_from(Category))
        total = total_result.scalar_one()
        return items_result.scalars().all(), total

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(
            name=data.name,
            description=data.description,
            is_active=data.is_active if data.is_active is not None else True,
        )
        self._session.add(category)
        await self._session.flush()
        await self._session.refresh(category)
        return category

    async def update(self, category: Category, data: CategoryUpdate) -> Category:
        if data.name is not None:
            category.name = data.name
        if data.description is not None:
            category.description = data.description
        if data.is_active is not None:
            category.is_active = data.is_active
        await self._session.flush()
        await self._session.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        await self._session.delete(category)
        await self._session.flush()