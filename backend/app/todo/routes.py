import typing

from app.todo.views import (
    ToDoAddView,
    ToDoListView,
    ToDoUpdateView,
    #ToDoDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/todo.add", ToDoAddView)
    app.router.add_view("/todo.update", ToDoUpdateView)
    #app.router.add_view("/todo.delete", ToDoDeleteView)
    app.router.add_view("/todo.list", ToDoListView)