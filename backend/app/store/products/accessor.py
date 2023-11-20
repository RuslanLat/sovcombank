import typing
from typing import List, Optional
from sqlalchemy import select, update, delete

from app.products.models import Product, ProductModel
from app.base.base_accessor import BaseAccessor


class ProductAccessor(BaseAccessor):
    async def get_by_product(self, product: str) -> Optional[Product]:
        async with self.app.database.session() as session:
            query = select(ProductModel).where(ProductModel.product == product)
            product: Optional[ProductModel] = await session.scalar(query)

        if not product:
            return None

        return Product(id=product.id, product=product.product, description=product.description)

    async def get_by_product_id(self, id: int) -> Optional[Product]:
        async with self.app.database.session() as session:
            query = select(ProductModel).where(ProductModel.id == id)
            product: Optional[ProductModel] = await session.scalar(query)

        if not product:
            return None

        return Product(id=product.id, product=product.product, description=product.description)

    async def create_product(self, product: str, description: str) -> Optional[Product]:
        new_product: Product = ProductModel(problem=product, description=description)

        async with self.app.database.session.begin() as session:
            session.add(new_product)

        return Product(id=new_product.id, product=new_product.product, description=new_product.description)

    async def update_product(self, id: int, product: str) -> Optional[Product]:
        query = (
            update(ProductModel)
            .where(ProductModel.id == id)
            .values(problem=product)
            .returning(ProductModel)
        )

        async with self.app.database.session.begin() as session:
            product = await session.scalar(query)

        if not product:
            return None

        return Product(id=product.id, product=product.product, description=product.description)

    async def delete_product(self, product: str) -> Optional[Product]:
        query = delete(ProductModel).where(ProductModel.product == product).returning(ProductModel)

        async with self.app.database.session.begin() as session:
            product = await session.scalar(query)

        if not product:
            return None

        return Product(id=product.id, product=product.product, description=product.description)

    async def list_products(self) -> List[Optional[Product]]:
        query = select(ProductModel)

        async with self.app.database.session() as session:
            products = await session.scalars(query)

        if not products:
            return []

        return [Product(id=product.id, product=product.product, description=product.description) for product in products.all()]