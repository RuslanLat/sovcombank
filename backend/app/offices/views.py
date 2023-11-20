from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.offices.schemes import (
    OfficeRequestSchema,
    OfficeSchema,
    OfficeIdResponseSchema,
    OfficeResponseSchema,
    OfficeListResponseSchema,
    OfficeIdListResponseSchema
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.offices.models import OfficeId, Office
from app.addresses.models import Addresse
from app.store.geocoder.dataclasses import PointAddresse, PointCoordinates


class OfficeAddView(AuthUserRequiredMixin, View):
    @request_schema(OfficeRequestSchema)
    @response_schema(OfficeResponseSchema, 200)
    @docs(
        tags=["offices"],
        summary="Add office add view",
        description="Add office to database",
    )
    async def post(self) -> Response:
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]

        try:
            office: Office = await self.store.offices.create_office(
                city=city, addresse=addresse
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=OfficeResponseSchema().dump(office))


class OfficeDeleteView(AuthUserRequiredMixin, View):
    @request_schema(OfficeRequestSchema)
    @response_schema(OfficeIdResponseSchema, 200)
    @docs(
        tags=["offices"],
        summary="Add office delete view",
        description="Delete office from database",
    )
    async def delete(self) -> Response:
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]

        office: OfficeId = await self.store.offices.delete_office(
            city=city, addresse=addresse
        )

        return json_response(data=OfficeIdResponseSchema().dump(office))


class OfficeListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(OfficeListResponseSchema, 200)
    @docs(
        tags=["offices"],
        summary="Add offices list view",
        description="Get list offices from database",
    )
    async def get(self) -> Response:
        offices: List[Office] = await self.store.offices.list_offices()
        return json_response(
            OfficeListResponseSchema().dump({"offices": offices})
        )
