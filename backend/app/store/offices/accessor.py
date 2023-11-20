import typing
from typing import List, Optional
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload
from app.offices.models import Office, OfficeId, OfficeModel
from app.addresses.models import AddresseModel
from app.base.base_accessor import BaseAccessor


class OfficeAccessor(BaseAccessor):
    async def create_id_office(
        self,
        city: str,
        addresse: str,
    ) -> Optional[OfficeId]:
        addresse = await self.app.store.addresses.get_by_addresse(
            city=city, addresse=addresse
        )

        new_office: OfficeModel = OfficeModel(addresse_id=addresse.id)

        async with self.app.database.session.begin() as session:
            session.add(new_office)

        return OfficeId(id=new_office.id, addresse_id=new_office.addresse_id)

    async def create_office(
        self,
        city: str,
        addresse: str,
    ) -> Optional[OfficeId]:
        addresse = await self.app.store.addresses.get_by_addresse(
            city=city, addresse=addresse
        )

        new_office: OfficeModel = OfficeModel(addresse_id=addresse.id)

        async with self.app.database.session.begin() as session:
            session.add(new_office)

        query = (
            select(OfficeModel)
            .where(OfficeModel.id == new_office.id)
            .options(joinedload(OfficeModel.addresse))
        )

        async with self.app.database.session.begin() as session:
            office = await session.scalar(query)

        return Office(
            id=office.id,
            city=office.city,
            addresse=office.addresse,
            lon=office.lon,
            lat=office.lat,
        )

    async def get_id_office(self, city: str, addresse: str) -> Optional[Office]:
        query = (
            select(AddresseModel)
            .where(and_(AddresseModel.city == city, AddresseModel.addresse == addresse))
            .options(joinedload(AddresseModel.office))
        )

        async with self.app.database.session.begin() as session:
            addresse = await session.scalar(query)

        if not addresse:
            return None

        return OfficeId(id=addresse.office[0].id, addresse_id=addresse.id)

    async def delete_office(self, city: str, addresse: str) -> Optional[Office]:
        addresse = await self.app.store.addresses.get_by_addresse(
            city=city, addresse=addresse
        )

        query = (
            delete(OfficeModel)
            .where(OfficeModel.addresse_id == addresse.id)
            .returning(OfficeModel)
        )

        async with self.app.database.session.begin() as session:
            office = await session.scalar(query)

        if not office:
            return None

        return OfficeId(id=office.id, addresse_id=office.addresse_id)

    async def delete_id_office(self, id: int) -> Optional[OfficeId]:
        query = delete(OfficeModel).where(OfficeModel.id == id).returning(OfficeModel)

        async with self.app.database.session.begin() as session:
            office = await session.scalar(query)

        if not office:
            return None

        return OfficeId(id=office.id, addresse_id=office.addresse_id)

    async def list_id_offices(self) -> List[Optional[OfficeId]]:
        query = select(OfficeModel)

        async with self.app.database.session() as session:
            offices = await session.scalars(query)

        if not offices:
            return []

        return [
            OfficeId(id=office.id, addresse_id=office.addresse_id)
            for office in offices.all()
        ]

    async def list_offices(self) -> List[Optional[Office]]:
        query = select(OfficeModel).options(joinedload(OfficeModel.addresse))

        async with self.app.database.session() as session:
            offices = await session.scalars(query)

        if not offices:
            return []

        return [
            Office(
                id=office.id,
                city=office.addresse.city,
                addresse=office.addresse.addresse,
                lat=office.addresse.lat,
                lon=office.addresse.lon,
            )
            for office in offices.all()
        ]
