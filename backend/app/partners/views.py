from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.partners.schemes import (
    PartnerRequestSchema,
    PartnerResponseSchema,
    PartnerDeleteRequestSchema,
    PartnerIdDeleteResponseSchema,
    PartnerIdListResponseSchema,
    PartnerListResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.partners.models import Partner


class PartnerAddView(AuthUserRequiredMixin, View):
    @request_schema(PartnerRequestSchema)
    @response_schema(PartnerResponseSchema, 200)
    @docs(
        tags=["partners"],
        summary="Add partner add view",
        description="Add partner to database",
    )
    async def post(self) -> Response:
        partner: str = self.data["partner"]
        data_connect: str = self.data["data_connect"]
        city: str = self.data["city"]
        addresse: str = self.data["addresse"]

        try:
            partner: Partner = await self.store.partners.create_partner(
                partner=partner, data_connect=data_connect, city=city, addresse=addresse
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=PartnerResponseSchema().dump(partner))


class PartnerUpdateView(AuthUserRequiredMixin, View):
    @request_schema(PartnerResponseSchema)
    @response_schema(PartnerResponseSchema, 200)
    @docs(
        tags=["partners"],
        summary="Add partner update view",
        description="Update partner in database",
    )
    async def put(self) -> Response:
        partner: str = self.data["partner"]
        id: int = self.data["id"]

        try:
            partner: Partner = await self.store.partners.update_partner(
                id=id, partner=partner
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=PartnerResponseSchema().dump(partner))


class PartnerDeleteView(AuthUserRequiredMixin, View):
    @request_schema(PartnerDeleteRequestSchema)
    @response_schema(PartnerResponseSchema, 200)
    @docs(
        tags=["partners"],
        summary="Add partner delete view",
        description="Delete partner from database",
    )
    async def delete(self) -> Response:
        partner: str = self.data["partner"]

        partner: Partner = await self.store.partners.delete_partner(partner=partner)

        return json_response(data=PartnerResponseSchema().dump(partner))


class PartnerListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(PartnerListResponseSchema, 200)
    @docs(
        tags=["partners"],
        summary="Add partner list view",
        description="Get list partners from database",
    )
    async def get(self) -> Response:
        partners: List[Partner] = await self.store.partners.list_partners()
        return json_response(PartnerListResponseSchema().dump({"partners": partners}))
