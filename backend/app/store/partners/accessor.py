import typing
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from app.partners.models import Partner, PartnerId, PartnerModel
from app.base.base_accessor import BaseAccessor


class PartnerAccessor(BaseAccessor):
    async def get_by_partner(self, partner: str) -> Optional[PartnerId]:
        async with self.app.database.session() as session:
            query = select(PartnerModel).where(PartnerModel.partner == partner)
            partner: Optional[PartnerModel] = await session.scalar(query)

        if not partner:
            return None

        return PartnerId(
            id=partner.id,
            partner=partner.partner,
            data_connect=partner.data_connect,
            addresse_id=partner.addresse_id,
        )

    async def get_by_partner_id(self, id: int) -> Optional[Partner]:
        async with self.app.database.session() as session:
            query = select(PartnerModel).where(PartnerModel.id == id)
            partner: Optional[PartnerModel] = await session.scalar(query)

        if not partner:
            return None

        return PartnerId(
            id=partner.id,
            partner=partner.partner,
            data_connect=partner.data_connect,
            addresse_id=partner.addresse_id,
        )

    async def create_partner(
        self, partner: str, data_connect: str, city: str, addresse: str
    ) -> Optional[Partner]:
        addresse = await self.app.store.addresses.get_by_addresse(
            city=city, addresse=addresse
        )
        new_partner: Partner = PartnerModel(
            partner=partner, data_connect=data_connect, addresse_id=addresse.id
        )

        async with self.app.database.session.begin() as session:
            session.add(new_partner)

        return PartnerId(
            id=new_partner.id,
            partner=new_partner.partner,
            data_connect=new_partner.data_connect,
            addresse_id=new_partner.addresse_id,
        )

    async def update_partner(self, id: int, partner: str) -> Optional[Partner]:
        query = (
            update(PartnerModel)
            .where(PartnerModel.id == id)
            .values(partner=partner)
            .returning(PartnerModel)
        )

        async with self.app.database.session.begin() as session:
            partner = await session.scalar(query)

        if not partner:
            return None

        return PartnerId(
            id=partner.id,
            partner=partner.partner,
            data_connect=partner.data_connect,
            addresse_id=partner.addresse_id,
        )

    async def delete_partner(self, partner: str) -> Optional[Partner]:
        query = (
            delete(PartnerModel)
            .where(PartnerModel.partner == partner)
            .returning(PartnerModel)
        )

        async with self.app.database.session.begin() as session:
            partner = await session.scalar(query)

        if not partner:
            return None

        return PartnerId(
            id=partner.id,
            partner=partner.partner,
            data_connect=partner.data_connect,
            addresse_id=partner.addresse_id,
        )

    async def list_id_partners(self) -> List[Optional[PartnerId]]:
        query = select(PartnerModel)

        async with self.app.database.session() as session:
            partners = await session.scalars(query)

        if not partners:
            return []

        return [
            PartnerId(
                id=partner.id,
                partner=partner.partner,
                data_connect=partner.data_connect,
                addresse_id=partner.addresse_id,
            )
            for partner in partners.all()
        ]

    async def list_partners(self) -> List[Optional[Partner]]:
        query = select(PartnerModel).options(joinedload(PartnerModel.addresse))

        async with self.app.database.session() as session:
            partners = await session.scalars(query)

        if not partners:
            return []

        return [
            Partner(
                id=partner.id,
                partner=partner.partner,
                data_connect=partner.data_connect,
                city=partner.addresse.city,
                addresse=partner.addresse.addresse,
                lat=partner.addresse.lat,
                lon=partner.addresse.lon
            )
            for partner in partners.all()
        ]
