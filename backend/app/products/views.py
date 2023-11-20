from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.products.schemes import (
    ProductRequestSchema,
    ProductResponseSchema,
    ProductListResponseSchema,
    ProductDeleteRequestSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.products.models import Product


class ProductAddView(AuthUserRequiredMixin, View):
    @request_schema(ProductRequestSchema)
    @response_schema(ProductResponseSchema, 200)
    @docs(
        tags=["products"],
        summary="Add product add view",
        description="Add product to database",
    )
    async def post(self) -> Response:
        product: str = self.data["product"]
        description: str = self.data["description"]

        try:
            product: Product = await self.store.products.create_product(
                product=product, description=description
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=ProductResponseSchema().dump(product))


class ProductUpdateView(AuthUserRequiredMixin, View):
    @request_schema(ProductResponseSchema)
    @response_schema(ProductResponseSchema, 200)
    @docs(
        tags=["products"],
        summary="Add product update view",
        description="Update product in database",
    )
    async def put(self) -> Response:
        product: str = self.data["product"]
        description: str = self.data["description"]
        id: int = self.data["id"]

        try:
            product: Product = await self.store.products.update_product(
                id=id, product=product, description=description
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=ProductResponseSchema().dump(product))


class ProductDeleteView(AuthUserRequiredMixin, View):
    @request_schema(ProductDeleteRequestSchema)
    @response_schema(ProductResponseSchema, 200)
    @docs(
        tags=["products"],
        summary="Add product delete view",
        description="Delete product from database",
    )
    async def delete(self) -> Response:
        product: str = self.data["product"]

        product: Product = await self.store.products.delete_product(product=product)

        return json_response(data=ProductResponseSchema().dump(product))


class ProductListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(ProductListResponseSchema, 200)
    @docs(
        tags=["products"],
        summary="Add product list view",
        description="Get list products from database",
    )
    async def get(self) -> Response:
        products: List[Product] = await self.store.products.list_products()
        return json_response(ProductListResponseSchema().dump({"products": products}))
