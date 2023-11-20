from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.addresses.schemes import (
    AddresseRequestSchema,
    AddresseResponseSchema,
    AddresseListResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.addresses.models import Addresse
from app.store.geocoder.dataclasses import PointAddresse, PointCoordinates


class AddresseAddView(AuthUserRequiredMixin, View):
    @request_schema(AddresseRequestSchema)
    @response_schema(AddresseResponseSchema, 200)
    @docs(
        tags=["addresses"],
        summary="Add addresse add view",
        description="Add addresse to database",
    )
    async def post(self) -> Response:
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]

        coordinates: PointCoordinates = await self.store.geocoder.get_geo_point(
            PointAddresse(city=city, addresse=addresse)
        )

        try:
            addresse: Addresse = await self.store.addresses.create_addresse(
                city=city, addresse=addresse, lon=coordinates.lon, lat=coordinates.lat
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=AddresseResponseSchema().dump(addresse))


class AddresseUpdateView(AuthUserRequiredMixin, View):
    @request_schema(AddresseResponseSchema)
    @response_schema(AddresseResponseSchema, 200)
    @docs(
        tags=["addresses"],
        summary="Add addresse update view",
        description="Update addresse in database",
    )
    async def put(self) -> Response:
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]
        id: int = self.data["id"]

        try:
            addresse: Addresse = await self.store.addresses.update_addresse(
                id=id, city=city, addresse=addresse
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=AddresseResponseSchema().dump(addresse))


class AddresseDeleteView(AuthUserRequiredMixin, View):
    @request_schema(AddresseRequestSchema)
    @response_schema(AddresseResponseSchema, 200)
    @docs(
        tags=["addresses"],
        summary="Add addresse delete view",
        description="Delete addresse from database",
    )
    async def delete(self) -> Response:
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]

        addresse: Addresse = await self.store.addresses.delete_addresse(
            city=city, addresse=addresse
        )

        return json_response(data=AddresseResponseSchema().dump(addresse))


class AddresseListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(AddresseListResponseSchema, 200)
    @docs(
        tags=["addresses"],
        summary="Add addresse list view",
        description="Get list addresses from database",
    )
    async def get(self) -> Response:
        addresses: List[Addresse] = await self.store.addresses.list_addresses()
        return json_response(
            AddresseListResponseSchema().dump({"addresses": addresses})
        )
