import typing
from typing import List, Optional
from sqlalchemy import select, update, delete, and_

from app.addresses.models import Addresse, AddresseModel
from app.base.base_accessor import BaseAccessor


class AddresseAccessor(BaseAccessor):
    async def get_by_addresse(self, city: str, addresse: str) -> Optional[Addresse]:
        async with self.app.database.session() as session:
            query = select(AddresseModel).where(
                and_(AddresseModel.city == city, AddresseModel.addresse == addresse)
            )
            addresse: Optional[AddresseModel] = await session.scalar(query)

        if not addresse:
            return None

        return Addresse(
            id=addresse.id,
            city=addresse.city,
            addresse=addresse.addresse,
            lon=addresse.lon,
            lat=addresse.lat,
        )

    async def get_by_addresse_id(self, id: int) -> Optional[Addresse]:
        async with self.app.database.session() as session:
            query = select(AddresseModel).where(AddresseModel.id == id)
            addresse: Optional[AddresseModel] = await session.scalar(query)

        if not addresse:
            return None

        return Addresse(
            id=addresse.id,
            city=addresse.city,
            addresse=addresse.addresse,
            lon=addresse.lon,
            lat=addresse.lat,
        )

    async def create_addresse(
        self, city: str, addresse: str, lon: float, lat: float
    ) -> Optional[Addresse]:
        new_addresse: AddresseModel = AddresseModel(
            city=city, addresse=addresse, lon=lon, lat=lat
        )

        async with self.app.database.session.begin() as session:
            session.add(new_addresse)

        return Addresse(
            id=new_addresse.id,
            city=new_addresse.city,
            addresse=new_addresse.addresse,
            lon=new_addresse.lon,
            lat=new_addresse.lat,
        )

    # async def update_addresse(self, id: int, partner: str) -> Optional[Partner]:
    #     query = (
    #         update(PartnerModel)
    #         .where(PartnerModel.id == id)
    #         .values(partner=partner)
    #         .returning(PartnerModel)
    #     )

    #     async with self.app.database.session.begin() as session:
    #         partner = await session.scalar(query)

    #     if not partner:
    #         return None

    #     return Partner(id=partner.id, partner=partner.partner)

    async def delete_addresse(self, city: str, addresse: str) -> Optional[Addresse]:
        query = (
            delete(AddresseModel)
            .where(and_(AddresseModel.city == city, AddresseModel.addresse == addresse))
            .returning(AddresseModel)
        )

        async with self.app.database.session.begin() as session:
            addresse = await session.scalar(query)

        if not addresse:
            return None

        return Addresse(
            id=addresse.id,
            city=addresse.city,
            addresse=addresse.addresse,
            lon=addresse.lon,
            lat=addresse.lat,
        )

    async def list_addresses(self) -> List[Optional[Addresse]]:
        query = select(AddresseModel)

        async with self.app.database.session() as session:
            addresses = await session.scalars(query)

        if not addresses:
            return []

        return [
            Addresse(
            id=addresse.id,
            city=addresse.city,
            addresse=addresse.addresse,
            lon=addresse.lon,
            lat=addresse.lat,
        )
            for addresse in addresses.all()
        ]
