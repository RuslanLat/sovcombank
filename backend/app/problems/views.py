from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.problems.schemes import (
    ProblemRequestSchema,
    ProblemResponseSchema,
    ProblemListResponseSchema,
    ProblemDeleteRequestSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.problems.models import Problem


class ProblemAddView(AuthUserRequiredMixin, View):
    @request_schema(ProblemRequestSchema)
    @response_schema(ProblemResponseSchema, 200)
    @docs(
        tags=["problems"],
        summary="Add problem add view",
        description="Add problem to database",
    )
    async def post(self) -> Response:
        problem_type: int = self.data["problem_type"]
        problem: str = self.data["problem"]
        priority: str = self.data["priority"]
        lead_time: str = self.data["lead_time"]
        condition_one: str = self.data["condition_one"]
        condition_two: str = self.data["condition_two"]
        rank: str = self.data["rank"]

        try:
            problem: Problem = await self.store.problems.create_problem(
                problem_type=problem_type,
                problem=problem,
                priority=priority,
                lead_time=lead_time,
                condition_one=condition_one,
                condition_two=condition_two,
                rank=rank,
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=ProblemResponseSchema().dump(problem))


class ProblemUpdateView(AuthUserRequiredMixin, View):
    @request_schema(ProblemResponseSchema)
    @response_schema(ProblemResponseSchema, 200)
    @docs(
        tags=["problems"],
        summary="Add problem update view",
        description="Update problem in database",
    )
    async def put(self) -> Response:
        problem: str = self.data["problem"]
        id: int = self.data["id"]

        try:
            problem: Problem = await self.store.problems.update_problem(
                id=id, problem=problem
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=ProblemResponseSchema().dump(problem))


class ProblemDeleteView(AuthUserRequiredMixin, View):
    @request_schema(ProblemDeleteRequestSchema)
    @response_schema(ProblemResponseSchema, 200)
    @docs(
        tags=["problems"],
        summary="Add problem delete view",
        description="Delete problem from database",
    )
    async def delete(self) -> Response:
        problem: str = self.data["problem"]

        problem: Problem = await self.store.problems.delete_problem(problem=problem)

        return json_response(data=ProblemResponseSchema().dump(problem))


class ProblemListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(ProblemListResponseSchema, 200)
    @docs(
        tags=["problems"],
        summary="Add problem list view",
        description="Get list problems from database",
    )
    async def get(self) -> Response:
        problems: List[Problem] = await self.store.problems.list_problems()
        return json_response(ProblemListResponseSchema().dump({"problems": problems}))
