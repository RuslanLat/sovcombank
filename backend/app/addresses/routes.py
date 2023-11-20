import typing

from app.addresses.views import (
    AddresseAddView,
    AddresseListView,
    AddresseUpdateView,
    AddresseDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/addresse.add", AddresseAddView)
    app.router.add_view("/addresse.update", AddresseUpdateView)
    app.router.add_view("/addresse.delete", AddresseDeleteView)
    app.router.add_view("/addresse.list", AddresseListView)