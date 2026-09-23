"""
Esquemas Pydantic para la entidad Category.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)