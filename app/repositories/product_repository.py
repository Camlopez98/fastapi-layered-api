"""
Repositorio de Producto (patrón Repository).

Mismo patrón que `UserRepository`: consultas SQLAlchemy asíncronas y solo
`flush()`; el commit lo hace `get_db()` al final de la petición.
"""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        return await self._session.get(Product, product_id)

    async def list(self, *, offset: int = 0, limit: int = 100) -> Sequence[Product]:
        result = await self._session.execute(
            select(Product).order_by(Product.id).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self._session.add(product)
        await self._session.flush()  # asigna el `id` sin cerrar la transacción
        await self._session.refresh(product)
        return product

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self._session.flush()
        await self._session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self._session.delete(product)
        await self._session.flush()
