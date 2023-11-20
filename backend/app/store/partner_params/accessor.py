import typing
from typing import List, Optional
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload

from app.partner_params.models import PartnerParam, PartnerParamId, PartnerParamModel
from app.partners.models import PartnerModel
from app.base.base_accessor import BaseAccessor


class PartnerParamAccessor(BaseAccessor):
    async def create_partner_param(
        self,
        partner: str,
        delivered: bool,
        num_days: int,
        num_applications: int,
        num_cards: int,
    ) -> Optional[PartnerParamId]:
        partner = await self.app.store.partners.get_by_partner(partner=partner)
        new_partner_param = PartnerParamModel(
            partner_id=partner.id,
            delivered=delivered,
            num_days=num_days,
            num_applications=num_applications,
            num_cards=num_cards,
        )

        async with self.app.database.session.begin() as session:
            session.add(new_partner_param)

        return PartnerParamId(
            id=new_partner_param.id,
            created_at=new_partner_param.created_at,
            partner_id=new_partner_param.partner_id,
            delivered=new_partner_param.delivered,
            num_days=new_partner_param.num_days,
            num_applications=new_partner_param.num_applications,
            num_cards=new_partner_param.num_cards,
        )

    async def delete_partner_param(self, id: int) -> Optional[PartnerParamId]:
        query = (
            delete(PartnerParamModel)
            .where(PartnerParamModel.id == id)
            .returning(PartnerParamModel)
        )

        async with self.app.database.session.begin() as session:
            partner_param = await session.scalar(query)

        if not partner_param:
            return None

        return PartnerParamId(
            id=partner_param.id,
            created_at=partner_param.created_at,
            partner_id=partner_param.partner_id,
            delivered=partner_param.delivered,
            num_days=partner_param.num_days,
            num_applications=partner_param.num_applications,
            num_cards=partner_param.num_cards,
        )

    async def list_partner_params(self) -> List[Optional[PartnerParam]]:
        query = (
            select(PartnerParamModel, PartnerModel)
            .options(joinedload(PartnerParamModel.partner))
            .options(joinedload(PartnerModel.addresse))
        )

        async with self.app.database.session() as session:
            partner_params = await session.scalars(query)

        if not partner_params:
            return []

        return [
            PartnerParam(
                id=partner_param.id,
                created_at=partner_param.created_at,
                partner=partner_param.partner.partner,
                city=partner_param.partner.addresse.city,
                addresse=partner_param.partner.addresse.addresse,
                data_connect=partner_param.partner.data_connect,
                delivered=partner_param.delivered,
                num_days=partner_param.num_days,
                num_applications=partner_param.num_applications,
                num_cards=partner_param.num_cards,
            )
            for partner_param in partner_params.unique()
        ]
