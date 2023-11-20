from typing import List
from aiohttp.web import (
    HTTPForbidden,
    HTTPUnauthorized,
    HTTPConflict,
)
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.jobs.schemes import (
    UserJobRequestSchema,
    UserJobIdResponseSchema,
    UserJobResponseSchema,
    UserJobIdListResponseSchema,
    UserJobListResponseSchema,
    UserJobDeleteResponseSchema,
    UserJobIdDeleteResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.jobs.models import UserJob, UserJobId


class UserJobIdAddView(AuthUserRequiredMixin, View):
    @request_schema(UserJobRequestSchema)
    @response_schema(UserJobIdResponseSchema, 200)
    @docs(
        tags=["jobs"],
        summary="Add job add view",
        description="Add job to database",
    )
    async def post(self) -> Response:
        surname: str = self.data["surname"]
        name: str = self.data["name"]
        patronymic: str = self.data["patronymic"]
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]
        rank: str = self.data["rank"]
        position: str = self.data["position"]

        try:
            user_job: UserJobId = await self.store.jobs.create_id_job(
                surname=surname,
                name=name,
                patronymic=patronymic,
                city=city,
                addresse=addresse,
                rank=rank,
                position=position,
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=UserJobIdResponseSchema().dump(user_job))


class UserJobAddView(AuthUserRequiredMixin, View):
    @request_schema(UserJobRequestSchema)
    @response_schema(UserJobResponseSchema, 200)
    @docs(
        tags=["jobs"],
        summary="Add job add view",
        description="Add job to database",
    )
    async def post(self) -> Response:
        surname: str = self.data["surname"]
        name: str = self.data["name"]
        patronymic: str = self.data["patronymic"]
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]
        rank: str = self.data["rank"]
        position: str = self.data["position"]

        try:
            user_job: UserJob = await self.store.jobs.create_job(
                surname=surname,
                name=name,
                patronymic=patronymic,
                city=city,
                addresse=addresse,
                rank=rank,
                position=position,
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=UserJobResponseSchema().dump(user_job))


class UserJobIdDeleteView(AuthUserRequiredMixin, View):
    @request_schema(UserJobIdDeleteResponseSchema)
    @response_schema(UserJobIdResponseSchema, 200)
    @docs(
        tags=["jobs"],
        summary="Add job delete view",
        description="Delete job from database",
    )
    async def delete(self) -> Response:
        id: int = self.data["id"]

        job: UserJobId = await self.store.jobs.delete_id_job(id=id)

        return json_response(data=UserJobIdResponseSchema().dump(job))


class UserJobDeleteView(AuthUserRequiredMixin, View):
    @request_schema(UserJobDeleteResponseSchema)
    @response_schema(UserJobIdResponseSchema, 200)
    @docs(
        tags=["jobs"],
        summary="Add job delete view",
        description="Delete job from database",
    )
    async def delete(self) -> Response:
        surname: str = self.data["surname"]
        name: str = self.data["name"]
        patronymic: str = self.data["patronymic"]

        job: UserJobId = await self.store.jobs.delete_job(
            surname=surname, name=name, patronymic=patronymic
        )

        return json_response(data=UserJobIdResponseSchema().dump(job))


class UserJobIdListView(AuthUserRequiredMixin, View):
    @response_schema(UserJobIdListResponseSchema, 200)
    @docs(
        tags=["jobs"],
        summary="Add job list view",
        description="Get list jobs from database",
    )
    async def get(self) -> Response:
        user_jobs = await self.store.jobs.list_id_jobs()
        return json_response(
            UserJobIdListResponseSchema().dump({"user_jobs": user_jobs})
        )


class UserJobListView(AuthUserRequiredMixin, View):
    @response_schema(UserJobListResponseSchema, 200)
    @docs(
        tags=["jobs"],
        summary="Add job list view",
        description="Get list jobs from database",
    )
    async def get(self) -> Response:
        user_jobs = await self.store.jobs.list_jobs()
        return json_response(UserJobListResponseSchema().dump({"user_jobs": user_jobs}))
