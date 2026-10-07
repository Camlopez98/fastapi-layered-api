"""
Router: Productos.

- Lectura pública (listar y consultar).
- Crear, actualizar y eliminar exigen un usuario autenticado y activo
  (OWASP API5:2023 Broken Function Level Authorization).
- Las excepciones de dominio del servicio se traducen aquí a HTTP.
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_active_user, get_product_service
from app.core.exceptions import InvalidProductPriceError, ProductNotFoundError
from app.models.user import User
from app.schemas.common import ErrorResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

ServiceDep = Annotated[ProductService, Depends(get_product_service)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]

NOT_FOUND = {404: {"model": ErrorResponse, "description": "Producto no encontrado"}}


def _not_found(error: ProductNotFoundError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


def _bad_price(error: InvalidProductPriceError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/", response_model=List[ProductResponse], summary="Listar productos (paginado)")
async def list_products(
    service: ServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return await service.list_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse, responses=NOT_FOUND)
async def get_product(product_id: int, service: ServiceDep):
    try:
        return await service.get_product(product_id)
    except ProductNotFoundError as error:
        raise _not_found(error)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, service: ServiceDep, _: CurrentUser):
    try:
        return await service.create_product(data)
    except InvalidProductPriceError as error:
        raise _bad_price(error)


@router.put("/{product_id}", response_model=ProductResponse, responses=NOT_FOUND)
async def update_product(
    product_id: int, data: ProductUpdate, service: ServiceDep, _: CurrentUser
):
    try:
        return await service.update_product(product_id, data)
    except ProductNotFoundError as error:
        raise _not_found(error)
    except InvalidProductPriceError as error:
        raise _bad_price(error)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND)
async def delete_product(product_id: int, service: ServiceDep, _: CurrentUser) -> None:
    try:
        await service.delete_product(product_id)
    except ProductNotFoundError as error:
        raise _not_found(error)
