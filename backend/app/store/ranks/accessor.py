import typing
from typing import List, Optional
from sqlalchemy import select, update, delete

from app.ranks.models import Rank, RankModel
from app.base.base_accessor import BaseAccessor


class RankAccessor(BaseAccessor):
    async def get_by_rank(self, rank: str) -> Optional[Rank]:
        async with self.app.database.session() as session:
            query = select(RankModel).where(RankModel.rank == rank)
            rank: Optional[RankModel] = await session.scalar(query)

        if not rank:
            return None

        return Rank(id=rank.id, rank=rank.rank)

    async def get_by_rank_id(self, id: int) -> Optional[Rank]:
        async with self.app.database.session() as session:
            query = select(RankModel).where(RankModel.id == id)
            rank: Optional[RankModel] = await session.scalar(query)

        if not rank:
            return None

        return Rank(id=rank.id, rank=rank.rank)

    async def create_rank(self, rank: str) -> Optional[Rank]:
        new_rank: Rank = RankModel(rank=rank)

        async with self.app.database.session.begin() as session:
            session.add(new_rank)

        return Rank(id=new_rank.id, rank=new_rank.rank)

    async def update_rank(self, id: int, rank: str) -> Optional[Rank]:
        query = (
            update(RankModel)
            .where(RankModel.id == id)
            .values(rank=rank)
            .returning(RankModel)
        )

        async with self.app.database.session.begin() as session:
            rank = await session.scalar(query)

        if not rank:
            return None

        return Rank(id=rank.id, rank=rank.rank)

    async def delete_rank(self, rank: str) -> Optional[Rank]:
        query = delete(RankModel).where(RankModel.rank == rank).returning(RankModel)

        async with self.app.database.session.begin() as session:
            rank = await session.scalar(query)

        if not rank:
            return None

        return Rank(id=rank.id, rank=rank.rank)

    async def list_ranks(self) -> List[Optional[Rank]]:
        query = select(RankModel)

        async with self.app.database.session() as session:
            ranks = await session.scalars(query)

        if not ranks:
            return []

        return [Rank(id=rank.id, rank=rank.rank) for rank in ranks.all()]
