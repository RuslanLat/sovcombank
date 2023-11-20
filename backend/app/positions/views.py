from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.positions.schemes import (
    PositionRequestSchema,
    PositionResponseSchema,
    PositionListResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.positions.models import Position


class PositionAddView(AuthUserRequiredMixin, View):
    @request_schema(PositionRequestSchema)
    @response_schema(PositionResponseSchema, 200)
    @docs(
        tags=["positions"],
        summary="Add position add view",
        description="Get position from database",
    )
    async def post(self) -> Response:
        position: str = self.data["position"]

        try:
            position: Position = await self.store.positions.create_position(
                position=position
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=PositionResponseSchema().dump(position))


class PositionUpdateView(AuthUserRequiredMixin, View):
    @request_schema(PositionResponseSchema)
    @response_schema(PositionResponseSchema, 200)
    @docs(
        tags=["positions"],
        summary="Add position update view",
        description="Update position in database",
    )
    async def put(self) -> Response:
        position: str = self.data["position"]
        id: int = self.data["id"]

        try:
            position: Position = await self.store.positions.update_position(
                id=id, position=position
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=PositionResponseSchema().dump(position))


class PositionDeleteView(AuthUserRequiredMixin, View):
    @request_schema(PositionRequestSchema)
    @response_schema(PositionResponseSchema, 200)
    @docs(
        tags=["positions"],
        summary="Add position delete view",
        description="Delete position from database",
    )
    async def delete(self) -> Response:
        position: str = self.data["position"]

        position: Position = await self.store.positions.delete_position(
            position=position
        )

        return json_response(data=PositionResponseSchema().dump(position))


class PositionListView(AuthUserRequiredMixin, View):
    @response_schema(PositionListResponseSchema, 200)
    @docs(
        tags=["positions"],
        summary="Add position list view",
        description="Get list positions from database",
    )
    async def get(self) -> Response:
        positions: List[Position] = await self.store.positions.list_positions()
        return json_response(
            PositionListResponseSchema().dump({"positions": positions})
        )
