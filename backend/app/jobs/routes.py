import typing

from app.jobs.views import (
    UserJobIdAddView,
    UserJobIdDeleteView,
    UserJobListView,
    UserJobIdListView,
    UserJobAddView,
    UserJobDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    from app.users.views import UserLoginView

    app.router.add_view("/job.id.add", UserJobIdAddView)
    app.router.add_view("/job.add", UserJobAddView)
    app.router.add_view("/job.id.delete", UserJobIdDeleteView)
    app.router.add_view("/job.delete", UserJobDeleteView)
    app.router.add_view("/job.list", UserJobListView)
    app.router.add_view("/job.id.list", UserJobIdListView)