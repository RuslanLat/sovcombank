import typing

from app.problems.views import (
    ProblemAddView,
    ProblemListView,
    ProblemUpdateView,
    ProblemDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/problem.add", ProblemAddView)
    app.router.add_view("/problem.update", ProblemUpdateView)
    app.router.add_view("/problem.delete", ProblemDeleteView)
    app.router.add_view("/problem.list", ProblemListView)