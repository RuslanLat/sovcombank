import typing

from app.ranks.views import (
    RankAddView,
    RankListView,
    RankUpdateView,
    RankDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/rank.add", RankAddView)
    app.router.add_view("/rank.update", RankUpdateView)
    app.router.add_view("/rank.delete", RankDeleteView)
    app.router.add_view("/rank.list", RankListView)
