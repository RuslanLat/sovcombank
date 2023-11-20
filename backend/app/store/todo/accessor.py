import typing
from typing import List, Optional
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload
from app.todo.models import ToDo, ToDoId, ToDoModel
from app.offices.models import OfficeModel
from app.users.models import UserModel
from app.jobs.models import UserJobModel
from app.partners.models import PartnerModel
from app.base.base_accessor import BaseAccessor


class ToDoAccessor(BaseAccessor):
    async def create_id_todo(
        self,
        user_id: int,
        office_id: int,
        partner_id: int,
        problem_id: int,
        queue: int,
        duration: float,
        length: float,
    ) -> Optional[ToDoId]:
        new_todo: ToDoModel = ToDoModel(
            user_id=user_id,
            office_id=office_id,
            partner_id=partner_id,
            problem_id=problem_id,
            queue=queue,
            duration=duration,
            length=length
        )

        async with self.app.database.session.begin() as session:
            session.add(new_todo)

        return ToDoId(
            id=new_todo.id,
            user_id=new_todo.user_id,
            office_id=new_todo.office_id,
            partner_id=new_todo.partner_id,
            problem_id=new_todo.problem_id,
            queue=new_todo.queue,
            status=new_todo.status,
            message=new_todo.message,
            duration=new_todo.duration,
            length=new_todo.length
        )

    # async def create_job(
    #     self,
    #     surname: str,
    #     name: str,
    #     patronymic: str,
    #     city: str,
    #     addresse: str,
    #     rank: str,
    #     position: str,
    # ) -> Optional[UserJob]:
    #     user = await self.app.store.users.get_by_full_name(
    #         surname=surname, name=name, patronymic=patronymic
    #     )
    #     position = await self.app.store.positions.get_by_position(position=position)
    #     rank = await self.app.store.ranks.get_by_rank(rank=rank)
    #     addresse = await self.app.store.addresses.get_by_addresse(
    #         city=city, addresse=addresse
    #     )
    #     new_job: UserJobModel = UserJobModel(
    #         user_id=user.id,
    #         addresse_id=addresse.id,
    #         position_id=position.id,
    #         rank_id=rank.id,
    #     )

    #     async with self.app.database.session.begin() as session:
    #         session.add(new_job)

    #     query = (
    #         select(UserJobModel)
    #         .where(UserJobModel.id == new_job.id)
    #         .options(joinedload(UserJobModel.rank))
    #         .options(joinedload(UserJobModel.position))
    #         .options(joinedload(UserJobModel.user))
    #         .options(joinedload(UserJobModel.addresse))
    #     )

    #     async with self.app.database.session.begin() as session:
    #         job = await session.scalar(query)

    #     return UserJob(
    #         id=job.id,
    #         surname=job.user.surname,
    #         name=job.user.name,
    #         patronymic=job.user.patronymic,
    #         city=job.addresse.city,
    #         addresse=job.addresse.addresse,
    #         lat=job.addresse.lon,
    #         lon=job.addresse.lat,
    #         position=job.position.position,
    #         rank=job.rank.rank,
    #     )

    async def update_todo(
        self, surname: str, name: str, patronymic: str, partner: str, message: str
    ) -> Optional[ToDoId]:
        user = await self.app.store.users.get_by_full_name(
            surname=surname, name=name, patronymic=patronymic
        )
        partner = await self.app.store.partners.get_by_partner(partner=partner)

        query = (
            update(ToDoModel)
            .where(
                and_(ToDoModel.user_id == user.id, ToDoModel.partner_id == partner.id)
            )
            .values(message=message, status=True)
            .returning(ToDoModel)
        )

        async with self.app.database.session.begin() as session:
            todo = await session.scalar(query)

        return ToDoId(
            id=todo.id,
            user_id=todo.user_id,
            office_id=todo.office_id,
            partner_id=todo.partner_id,
            problem_id=todo.problem_id,
            queue=todo.queue,
            status=todo.status,
            message=todo.message,
            duration=todo.duration,
            length=todo.length
        )

    # async def delete_id_job(self, id: int) -> Optional[UserJobId]:
    #     query = (
    #         delete(UserJobModel).where(UserJobModel.id == id).returning(UserJobModel)
    #     )

    #     async with self.app.database.session.begin() as session:
    #         job = await session.scalar(query)

    #     if not job:
    #         return None

    #     return UserJobId(
    #         id=job.id,
    #         user_id=job.user_id,
    #         addresse_id=job.addresse_id,
    #         position_id=job.position_id,
    #         rank_id=job.rank_id,
    #     )

    async def list_id_todo(self) -> List[Optional[ToDoId]]:
        query = select(ToDoModel)

        async with self.app.database.session() as session:
            todos = await session.scalars(query)

        if not todos:
            return []

        return [
            ToDoId(
                id=todo.id,
                user_id=todo.user_id,
                office_id=todo.office_id,
                partner_id=todo.partner_id,
                problem_id=todo.problem_id,
                queue=todo.queue,
                status=todo.status,
                message=todo.message,
                duration=todo.duration,
                length=todo.length
            )
            for todo in todos.all()
        ]

    async def list_todo(
        self, surname: str, name: str, patronymic: str
    ) -> List[Optional[ToDo]]:
        user = await self.app.store.users.get_by_full_name(
            surname=surname, name=name, patronymic=patronymic
        )

        query = (
            select(ToDoModel, PartnerModel, OfficeModel)
            .options(joinedload(ToDoModel.user))
            .options(joinedload(ToDoModel.office))
            .options(joinedload(ToDoModel.partner))
            .options(joinedload(ToDoModel.problem))
            .options(joinedload(PartnerModel.addresse))
            .options(joinedload(OfficeModel.addresse))
            .where(and_(ToDoModel.status == False, ToDoModel.user_id == user.id))
        )

        async with self.app.database.session() as session:
            todos = await session.scalars(query)

        if not todos:
            return []

        return [
            ToDo(
                id=todo.id,
                surname=todo.user.surname,
                name=todo.user.name,
                patronymic=todo.user.patronymic,
                city=todo.office.addresse.city,
                addresse=todo.office.addresse.addresse,
                lon=todo.office.addresse.lon,
                lat=todo.office.addresse.lat,
                partner=todo.partner.partner,
                partner_city=todo.partner.addresse.city,
                partner_addresse=todo.partner.addresse.addresse,
                partner_lon=todo.partner.addresse.lon,
                partner_lat=todo.partner.addresse.lat,
                problem=todo.problem.problem,
                queue=todo.queue,
                status=todo.status,
                message=todo.message,
                duration=todo.duration,
                length=todo.length
            )
            for todo in todos.unique()
        ]
