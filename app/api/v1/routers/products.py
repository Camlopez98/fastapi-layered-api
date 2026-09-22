from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.api.deps import get_product_service

# Prefijo para que todas las rutas empiecen con /products
# 'tags' sirve para que en Swagger se agrupen bajo el título "Products"
router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service),
):
    """Obtener lista paginada de productos."""
    return service.list_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Obtener un producto por su identificador (ID)."""
    return service.get_product(product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """Registrar un nuevo producto en la tienda."""
    return service.create_product(product_in)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Actualizar datos de un producto existente."""
    return service.update_product(product_id, product_in)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Eliminar un producto de la base de datos."""
    service.delete_product(product_id)
    return None