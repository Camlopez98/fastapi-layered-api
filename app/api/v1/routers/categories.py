"""
Router de la API para la entidad Categoria.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from ...deps import get_category_service, get_current_active_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


# ==========================================
# ENDPOINTS PÚBLICOS (Sin autenticación)
# ==========================================

@router.get("/", response_model=list[CategoryRead])
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
) -> Any:
    """Consulta pública del catálogo de categorías."""
    categories, _ = await service.list_categories(offset=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> Any:
    """Consulta pública de una categoría por su identificador."""
    category = await service.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


# ==========================================
# ENDPOINTS PROTEGIDOS (Con autenticación JWT)
# ==========================================

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: CategoryService = Depends(get_category_service),
) -> Any:
    """Creación protegida: requiere token JWT de usuario activo."""
    return await service.create_category(category_in)


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: CategoryService = Depends(get_category_service),
) -> Any:
    """Actualización protegida: requiere token JWT de usuario activo."""
    category = await service.update_category(category_id, category_in)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: CategoryService = Depends(get_category_service),
) -> None:
    """Eliminación protegida: requiere token JWT de usuario activo."""
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )