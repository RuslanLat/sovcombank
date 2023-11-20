from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.ranks.schemes import (
    RankRequestSchema,
    RankResponseSchema,
    RankListResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.ranks.models import Rank


class RankAddView(AuthUserRequiredMixin, View):
    @request_schema(RankRequestSchema)
    @response_schema(RankResponseSchema, 200)
    @docs(
        tags=["ranks"],
        summary="Add rank add view",
        description="Add rank to database",
    )
    async def post(self) -> Response:
        rank: str = self.data["rank"]

        try:
            rank: Rank = await self.store.ranks.create_rank(rank=rank)
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=RankResponseSchema().dump(rank))


class RankUpdateView(AuthUserRequiredMixin, View):
    @request_schema(RankResponseSchema)
    @response_schema(RankResponseSchema, 200)
    @docs(
        tags=["ranks"],
        summary="Add rank update view",
        description="Update rank in database",
    )
    async def put(self) -> Response:
        rank: str = self.data["rank"]
        id: int = self.data["id"]

        try:
            rank: Rank = await self.store.ranks.update_rank(id=id, rank=rank)
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=RankResponseSchema().dump(rank))


class RankDeleteView(AuthUserRequiredMixin, View):
    @request_schema(RankRequestSchema)
    @response_schema(RankResponseSchema, 200)
    @docs(
        tags=["ranks"],
        summary="Add rank delete view",
        description="Delete rank from database",
    )
    async def delete(self) -> Response:
        rank: str = self.data["rank"]

        rank: Rank = await self.store.ranks.delete_rank(rank=rank)

        return json_response(data=RankResponseSchema().dump(rank))


class RankListView(AuthUserRequiredMixin, View): #AuthRequiredMixin,
    @response_schema(RankListResponseSchema, 200)
    @docs(
        tags=["ranks"],
        summary="Add rank list view",
        description="Get list ranks from database",
    )
    async def get(self) -> Response:
        ranks: List[Rank] = await self.store.ranks.list_ranks()
        return json_response(RankListResponseSchema().dump({"ranks": ranks}))
