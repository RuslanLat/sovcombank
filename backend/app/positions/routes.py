import typing

from app.positions.views import (
    PositionAddView,
    PositionUpdateView,
    PositionDeleteView,
    PositionListView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/position.add", PositionAddView)
    app.router.add_view("/position.update", PositionUpdateView)
    app.router.add_view("/position.delete", PositionDeleteView)
    app.router.add_view("/position.list", PositionListView)
