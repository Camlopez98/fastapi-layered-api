"""
Servicio de dominio para la entidad Categoria.
"""

from typing import Optional, Sequence

from app.core.exceptions import DomainError
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        return await self.category_repo.get_by_id(category_id)

    async def get_by_name(self, name: str) -> Optional[Category]:
        return await self.category_repo.get_by_name(name)

    async def list_categories(
        self, offset: int = 0, limit: int = 20
    ) -> tuple[Sequence[Category], int]:
        return await self.category_repo.list(offset=offset, limit=limit)

    async def create_category(self, category_in: CategoryCreate) -> Category:
        existing = await self.category_repo.get_by_name(category_in.name)
        if existing:
            raise DomainError(f"Category with name '{category_in.name}' already exists.")
        return await self.category_repo.create(category_in)

    async def update_category(
        self, category_id: int, category_in: CategoryUpdate
    ) -> Optional[Category]:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            return None
        return await self.category_repo.update(category, category_in)

    async def delete_category(self, category_id: int) -> bool:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            return False
        await self.category_repo.delete(category)
        return True