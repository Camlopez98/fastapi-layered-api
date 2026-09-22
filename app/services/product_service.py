from typing import List
from fastapi import HTTPException, status
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con id {product_id} no existe",
            )
        return product

    def list_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.repository.get_all(skip=skip, limit=limit)

    def create_product(self, product_in: ProductCreate) -> Product:
        if product_in.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio del producto no puede ser negativo",
            )
        return self.repository.create(product_in)

    def update_product(self, product_id: int, product_in: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        if product_in.price is not None and product_in.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio del producto no puede ser negativo",
            )
        return self.repository.update(product, product_in)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.repository.delete(product)