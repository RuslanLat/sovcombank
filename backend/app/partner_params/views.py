from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.partner_params.schemes import (
    PartnerParamRequestSchema,
    PartnerParamIdResponseSchema,
    PartnerParamResponseSchema,
    PartnerParamIdDeleteResponseSchema,
    PartnerParamIdListResponseSchema,
    PartnerParamListResponseSchema,
    PartnerParamDeleteResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.partner_params.models import PartnerParam, PartnerParamId


class PartnerParamAddView(AuthUserRequiredMixin, View):
    @request_schema(PartnerParamRequestSchema)
    @response_schema(PartnerParamResponseSchema, 200)
    @docs(
        tags=["partner_params"],
        summary="Add partner param add view",
        description="Add partner param to database",
    )
    async def post(self) -> Response:
        partner: str = self.data["partner"]
        delivered: bool = self.data["delivered"]
        num_days: int = self.data["num_days"]
        num_applications: int = self.data["num_applications"]
        num_cards: int = self.data["num_cards"]

        try:
            partner_param: PartnerParam = (
                await self.store.partner_params.create_partner_param(
                    partner=partner,
                    delivered=delivered,
                    num_days=num_days,
                    num_applications=num_applications,
                    num_cards=num_cards,
                )
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=PartnerParamResponseSchema().dump(partner_param))


class PartnerParamDeleteView(AuthUserRequiredMixin, View):
    @request_schema(PartnerParamIdDeleteResponseSchema)
    @response_schema(PartnerParamResponseSchema, 200)
    @docs(
        tags=["partner_params"],
        summary="Add partner param delete view",
        description="Delete partner param from database",
    )
    async def delete(self) -> Response:
        id: int = self.data["id"]

        partner_param: PartnerParam = (
            await self.store.partner_params.delete_partner_param(id=id)
        )

        return json_response(data=PartnerParamResponseSchema().dump(partner_param))


class PartnerParamListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(PartnerParamListResponseSchema, 200)
    @docs(
        tags=["partner_params"],
        summary="Add partner param list view",
        description="Get list partner params from database",
    )
    async def get(self) -> Response:
        partner_params: List[
            PartnerParam
        ] = await self.store.partner_params.list_partner_params()
        return json_response(
            PartnerParamListResponseSchema().dump({"partner_params": partner_params})
        )
