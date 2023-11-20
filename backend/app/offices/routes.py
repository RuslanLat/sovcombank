import typing

from app.offices.views import (
    OfficeAddView,
    OfficeListView,
    OfficeDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/office.add", OfficeAddView)
    app.router.add_view("/office.delete", OfficeDeleteView)
    app.router.add_view("/office.list", OfficeListView)