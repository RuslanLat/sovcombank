import typing
from typing import List, Optional
from sqlalchemy import select, update, delete

from app.problems.models import Problem, ProblemModel
from app.base.base_accessor import BaseAccessor


class ProblemAccessor(BaseAccessor):
    async def get_by_problem(self, problem: str) -> Optional[Problem]:
        async with self.app.database.session() as session:
            query = select(ProblemModel).where(ProblemModel.problem == problem)
            problem: Optional[ProblemModel] = await session.scalar(query)

        if not problem:
            return None

        return Problem(
            id=problem.id,
            problem_type=problem.problem_type,
            problem=problem.problem,
            priority=problem.priority,
            lead_time=problem.lead_time,
            condition_one=problem.condition_one,
            condition_two=problem.condition_two,
            rank=problem.rank,
        )

    async def get_by_problem_id(self, id: int) -> Optional[Problem]:
        async with self.app.database.session() as session:
            query = select(ProblemModel).where(ProblemModel.id == id)
            problem: Optional[ProblemModel] = await session.scalar(query)

        if not problem:
            return None

        return Problem(
            id=problem.id,
            problem_type=problem.problem_type,
            problem=problem.problem,
            priority=problem.priority,
            lead_time=problem.lead_time,
            condition_one=problem.condition_one,
            condition_two=problem.condition_two,
            rank=problem.rank,
        )

    async def create_problem(
        self,
        problem_type: int,
        problem: str,
        priority: str,
        lead_time: str,
        condition_one: str,
        condition_two: str,
        rank: str,
    ) -> Optional[Problem]:
        new_problem: Problem = ProblemModel(
            problem_type=problem_type,
            problem=problem,
            priority=priority,
            lead_time=lead_time,
            condition_one=condition_one,
            condition_two=condition_two,
            rank=rank,
        )

        async with self.app.database.session.begin() as session:
            session.add(new_problem)

        return Problem(
            id=new_problem.id,
            problem_type=new_problem.problem_type,
            problem=new_problem.problem,
            priority=new_problem.priority,
            lead_time=new_problem.lead_time,
            condition_one=new_problem.condition_one,
            condition_two=new_problem.condition_two,
            rank=new_problem.rank,
        )

    async def update_problem(self, id: int, problem: str) -> Optional[Problem]:
        query = (
            update(ProblemModel)
            .where(ProblemModel.id == id)
            .values(problem=problem)
            .returning(ProblemModel)
        )

        async with self.app.database.session.begin() as session:
            problem = await session.scalar(query)

        if not problem:
            return None

        return Problem(
            id=problem.id,
            problem_type=problem.problem_type,
            problem=problem.problem,
            priority=problem.priority,
            lead_time=problem.lead_time,
            condition_one=problem.condition_one,
            condition_two=problem.condition_two,
            rank=problem.rank,
        )

    async def delete_problem(self, problem: str) -> Optional[Problem]:
        query = (
            delete(ProblemModel)
            .where(ProblemModel.problem == problem)
            .returning(ProblemModel)
        )

        async with self.app.database.session.begin() as session:
            problem = await session.scalar(query)

        if not problem:
            return None

        return Problem(
            id=problem.id,
            problem_type=problem.problem_type,
            problem=problem.problem,
            priority=problem.priority,
            lead_time=problem.lead_time,
            condition_one=problem.condition_one,
            condition_two=problem.condition_two,
            rank=problem.rank,
        )

    async def list_problems(self) -> List[Optional[Problem]]:
        query = select(ProblemModel)

        async with self.app.database.session() as session:
            problems = await session.scalars(query)

        if not problems:
            return []

        return [
            Problem(
                id=problem.id,
                problem_type=problem.problem_type,
                problem=problem.problem,
                priority=problem.priority,
                lead_time=problem.lead_time,
                condition_one=problem.condition_one,
                condition_two=problem.condition_two,
                rank=problem.rank,
            )
            for problem in problems.all()
        ]
