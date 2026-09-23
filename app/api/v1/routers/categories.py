from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_category_service
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse], summary="Consultar catalogo de categorias")
def get_categories(
    skip: int = 0,
    limit: int = 100,
    service: CategoryService = Depends(get_category_service),
):
    """Permite realizar consultas y paginacion sobre todas las categorias registradas."""
    return service.list_categories(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse, summary="Consultar categoria por ID")
def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    """Consulta detallada de una categoria especifica por su identificador."""
    return service.get_category(category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Registrar categoria")
def create_category(
    category_in: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(category_in)


@router.put("/{category_id}", response_model=CategoryResponse, summary="Actualizar categoria")
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return service.update_category(category_id, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar categoria")
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    service.delete_category(category_id)