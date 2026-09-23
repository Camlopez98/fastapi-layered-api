from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.db.query(Category).offset(skip).limit(limit).all()

    def create(self, category_in: CategoryCreate) -> Category:
        db_obj = Category(
            name=category_in.name,
            description=category_in.description,
            is_active=category_in.is_active,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Category, category_in: CategoryUpdate) -> Category:
        update_data = category_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Category) -> None:
        self.db.delete(db_obj)
        self.db.commit()