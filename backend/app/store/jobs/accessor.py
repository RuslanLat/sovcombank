import typing
from typing import List, Optional
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload
from app.jobs.models import (
    UserJobId,
    UserJob,
    UserJobModel,
)
from app.offices.models import OfficeModel
from app.base.base_accessor import BaseAccessor


class JobAccessor(BaseAccessor):
    # async def get_by_position(self, position: str) -> Optional[Position]:
    #     async with self.app.database.session() as session:
    #         query = select(PositionModel).where(PositionModel.position == position)
    #         position: Optional[PositionModel] = await session.scalar(query)

    #     if not position:
    #         return None

    #     return Position(id=position.id, position=position.position)

    # async def get_by_position_id(self, id: int) -> Optional[Position]:
    #     async with self.app.database.session() as session:
    #         query = select(PositionModel).where(PositionModel.id == id)
    #         position: Optional[PositionModel] = await session.scalar(query)

    #     if not position:
    #         return None

    #     return Position(id=position.id, position=position.position)

    async def create_id_job(
        self,
        surname: str,
        name: str,
        patronymic: str,
        city: str,
        addresse: str,
        rank: str,
        position: str,
    ) -> Optional[UserJobId]:
        user = await self.app.store.users.get_by_full_name(
            surname=surname, name=name, patronymic=patronymic
        )
        position = await self.app.store.positions.get_by_position(position=position)
        rank = await self.app.store.ranks.get_by_rank(rank=rank)
        office = await self.app.store.offices.get_id_office(city=city, addresse=addresse)
        
        new_job: UserJobModel = UserJobModel(
            user_id=user.id,
            office_id=office.id,
            position_id=position.id,
            rank_id=rank.id,
        )

        async with self.app.database.session.begin() as session:
            session.add(new_job)

        return UserJobId(
            id=new_job.id,
            user_id=new_job.user_id,
            office_id=new_job.office_id,
            position_id=new_job.position_id,
            rank_id=new_job.rank_id,
        )

    async def create_job(
        self,
        surname: str,
        name: str,
        patronymic: str,
        city: str,
        addresse: str,
        rank: str,
        position: str,
    ) -> Optional[UserJob]:
        user = await self.app.store.users.get_by_full_name(
            surname=surname, name=name, patronymic=patronymic
        )
        position = await self.app.store.positions.get_by_position(position=position)
        rank = await self.app.store.ranks.get_by_rank(rank=rank)
        addresse = await self.app.store.addresses.get_by_addresse(
            city=city, addresse=addresse
        )
        new_job: UserJobModel = UserJobModel(
            user_id=user.id,
            addresse_id=addresse.id,
            position_id=position.id,
            rank_id=rank.id,
        )

        async with self.app.database.session.begin() as session:
            session.add(new_job)

        query = (
            select(UserJobModel)
            .where(UserJobModel.id == new_job.id)
            .options(joinedload(UserJobModel.rank))
            .options(joinedload(UserJobModel.position))
            .options(joinedload(UserJobModel.user))
            .options(joinedload(UserJobModel.addresse))
        )

        async with self.app.database.session.begin() as session:
            job = await session.scalar(query)

        return UserJob(
            id=job.id,
            surname=job.user.surname,
            name=job.user.name,
            patronymic=job.user.patronymic,
            city=job.addresse.city,
            addresse=job.addresse.addresse,
            lat=job.addresse.lon,
            lon=job.addresse.lat,
            position=job.position.position,
            rank=job.rank.rank,
        )

    async def delete_job(
        self, surname: str, name: str, patronymic: str
    ) -> Optional[UserJobId]:
        user = await self.app.store.users.get_by_full_name(
            surname=surname, name=name, patronymic=patronymic
        )
        self.logger.info(user)
        query = (
            delete(UserJobModel)
            .where(UserJobModel.user_id == user.id)
            .returning(UserJobModel)
        )

        async with self.app.database.session.begin() as session:
            job = await session.scalar(query)

        if not job:
            return None

        return None

    async def delete_id_job(self, id: int) -> Optional[UserJobId]:
        query = (
            delete(UserJobModel).where(UserJobModel.id == id).returning(UserJobModel)
        )

        async with self.app.database.session.begin() as session:
            job = await session.scalar(query)

        if not job:
            return None

        return UserJobId(
            id=job.id,
            user_id=job.user_id,
            addresse_id=job.addresse_id,
            position_id=job.position_id,
            rank_id=job.rank_id,
        )

    async def list_id_jobs(self) -> List[Optional[UserJobId]]:
        query = select(UserJobModel)

        async with self.app.database.session() as session:
            jobs = await session.scalars(query)

        if not jobs:
            return []

        return [
            UserJobId(
                id=job.id,
                user_id=job.user_id,
                addresse_id=job.addresse_id,
                position_id=job.position_id,
                rank_id=job.rank_id,
            )
            for job in jobs.all()
        ]

    async def list_jobs(self) -> List[Optional[UserJob]]:
        query = (
            select(UserJobModel, OfficeModel)
            .options(joinedload(UserJobModel.rank))
            .options(joinedload(UserJobModel.position))
            .options(joinedload(UserJobModel.user))
            .options(joinedload(UserJobModel.office))
            .options(joinedload(OfficeModel.addresse, innerjoin=True))
        )

        async with self.app.database.session() as session:
            jobs = await session.scalars(query)

        if not jobs:
            return []

        return [
            UserJob(
            id=job.id,
            surname=job.user.surname,
            name=job.user.name,
            patronymic=job.user.patronymic,
            position=job.position.position,
            rank=job.rank.rank,
            city=job.office.addresse.city,
            addresse=job.office.addresse.addresse,
            lat=job.office.addresse.lon,
            lon=job.office.addresse.lat
        )
            for job in jobs.unique()
        ]
