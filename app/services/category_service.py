from typing import List
from fastapi import HTTPException, status
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def get_category(self, category_id: int) -> Category:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return category

    def list_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.category_repo.get_all(skip=skip, limit=limit)

    def create_category(self, category_in: CategoryCreate) -> Category:
        existing = self.category_repo.get_by_name(category_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_in.name}' already exists",
            )
        return self.category_repo.create(category_in)

    def update_category(self, category_id: int, category_in: CategoryUpdate) -> Category:
        category = self.get_category(category_id)
        return self.category_repo.update(category, category_in)

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        self.category_repo.delete(category)