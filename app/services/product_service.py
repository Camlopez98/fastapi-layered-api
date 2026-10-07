"""
Servicio de Producto (capa de lógica de negocio).

Aplica las reglas de negocio (el precio no puede ser negativo, el producto
debe existir) y lanza excepciones de dominio; no conoce HTTP. El router
traduce esas excepciones a códigos de estado.
"""

from typing import Optional, Sequence

from app.core.exceptions import InvalidProductPriceError, ProductNotFoundError
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    @staticmethod
    def _validate_price(price: Optional[float]) -> None:
        if price is not None and price < 0:
            raise InvalidProductPriceError("El precio del producto no puede ser negativo.")

    async def get_product(self, product_id: int) -> Product:
        product = await self._repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(f"El producto con id {product_id} no existe.")
        return product

    async def list_products(self, *, skip: int = 0, limit: int = 100) -> Sequence[Product]:
        return await self._repository.list(offset=skip, limit=limit)

    async def create_product(self, data: ProductCreate) -> Product:
        self._validate_price(data.price)
        return await self._repository.create(data)

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        self._validate_price(data.price)
        product = await self.get_product(product_id)
        return await self._repository.update(product, data)

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        await self._repository.delete(product)
