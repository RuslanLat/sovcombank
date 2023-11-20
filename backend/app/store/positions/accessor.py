import typing
from typing import List, Optional
from sqlalchemy import select, update, delete

from app.positions.models import Position, PositionModel
from app.base.base_accessor import BaseAccessor


class PositionAccessor(BaseAccessor):
    async def get_by_position(self, position: str) -> Optional[Position]:
        async with self.app.database.session() as session:
            query = select(PositionModel).where(PositionModel.position == position)
            position: Optional[PositionModel] = await session.scalar(query)

        if not position:
            return None

        return Position(id=position.id, position=position.position)

    async def get_by_position_id(self, id: int) -> Optional[Position]:
        async with self.app.database.session() as session:
            query = select(PositionModel).where(PositionModel.id == id)
            position: Optional[PositionModel] = await session.scalar(query)

        if not position:
            return None

        return Position(id=position.id, position=position.position)

    async def create_position(self, position: str) -> Optional[Position]:
        new_position: Position = PositionModel(position=position)

        async with self.app.database.session.begin() as session:
            session.add(new_position)

        return Position(id=new_position.id, position=new_position.position)

    async def update_position(self, id: int, position: str) -> Optional[Position]:
        query = (
            update(PositionModel)
            .where(PositionModel.id == id)
            .values(position=position)
            .returning(PositionModel)
        )

        async with self.app.database.session.begin() as session:
            position = await session.scalar(query)

        if not position:
            return None

        return Position(id=position.id, position=position.position)

    async def delete_position(self, position: str) -> Optional[Position]:
        query = (
            delete(PositionModel)
            .where(PositionModel.position == position)
            .returning(PositionModel)
        )

        async with self.app.database.session.begin() as session:
            position = await session.scalar(query)

        if not position:
            return None

        return Position(id=position.id, position=position.position)

    async def list_positions(self) -> List[Optional[Position]]:
        query = select(PositionModel)

        async with self.app.database.session() as session:
            positions = await session.scalars(query)

        if not positions:
            return []

        return [
            Position(id=position.id, position=position.position)
            for position in positions.all()
        ]
