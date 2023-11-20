import typing

from app.products.views import (
    ProductAddView,
    ProductListView,
    ProductUpdateView,
    ProductDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/product.add", ProductAddView)
    app.router.add_view("/product.update", ProductUpdateView)
    app.router.add_view("/product.delete", ProductDeleteView)
    app.router.add_view("/product.list", ProductListView)