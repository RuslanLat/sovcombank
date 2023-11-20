from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.todo.schemes import (
    ToDoRequestSchema,
    ToDoIdResponseSchema,
    ToDoResponseSchema,
    ToDoIdDeleteResponseSchema,
    ToDoIdListResponseSchema,
    ToDoListResponseSchema,
    ToDoUpdateRequestSchema,
    ToDoListeRequestSchema
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.todo.models import ToDo, ToDoId


class ToDoAddView(AuthUserRequiredMixin, View):
    @request_schema(ToDoRequestSchema)
    @response_schema(ToDoIdResponseSchema, 200)
    @docs(
        tags=["todo"],
        summary="Add todo add view",
        description="Add todo to database",
    )
    async def post(self) -> Response:
        user_id: int = self.data["user_id"]
        office_id: int = self.data["office_id"]
        partner_id: int = self.data["partner_id"]
        problem_id: int = self.data["problem_id"]
        queue: int = self.data["queue"]
        duration: float = self.data["duration"]
        length: float = self.data["length"]


        try:
            todo: ToDoId = await self.store.todo.create_id_todo(
                user_id=user_id,
                office_id=office_id,
                partner_id=partner_id,
                problem_id=problem_id,
                queue=queue,
                duration=duration,
                length=length
            )

        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=ToDoIdResponseSchema().dump(todo))


class ToDoUpdateView(AuthUserRequiredMixin, View):
    @request_schema(ToDoUpdateRequestSchema)
    @response_schema(ToDoResponseSchema, 200)
    @docs(
        tags=["todo"],
        summary="Add todo update view",
        description="Update todo from database",
    )
    async def put(self) -> Response:
        surname: str = self.data["surname"]
        name: str = self.data["name"]
        patronymic: str = self.data["patronymic"]
        partner: str = self.data["partner"]
        message: str = self.data["message"]

        todo: ToDoId = await self.store.todo.update_todo(
            surname=surname,
            name=name,
            patronymic=patronymic,
            partner=partner,
            message=message
        )

        return json_response(data=ToDoResponseSchema().dump(todo))


class ToDoIdListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(ToDoIdListResponseSchema, 200)
    @docs(
        tags=["todo"],
        summary="Add todo list view",
        description="Get list todo from database",
    )
    async def get(self) -> Response:
        todos: List[ToDo] = await self.store.todo.list_id_todo()
        return json_response(ToDoIdListResponseSchema().dump({"todos": todos}))
    

class ToDoListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(ToDoListeRequestSchema)
    @response_schema(ToDoListResponseSchema, 200)
    @docs(
        tags=["todo"],
        summary="Add todo list view",
        description="Get list todo from database",
    )
    async def get(self) -> Response:
         
        surname: str = self.data["surname"]
        name: str = self.data["name"]
        patronymic: str = self.data["patronymic"]

        todos: List[ToDo] = await self.store.todo.list_todo(surname, name, patronymic)
        return json_response(ToDoListResponseSchema().dump({"todos": todos}))


