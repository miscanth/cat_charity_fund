from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject, Donation


async def invest_donation(
        donation: Donation,
        session: AsyncSession,
):
    """Функция распределения пожертвований по незакрытым проектам."""
    not_invested_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        )
    )
    not_invested_projects = not_invested_projects.scalars().all()
    await investment_process(donation, not_invested_projects, session)


async def invest_update(
        project: CharityProject,
        session: AsyncSession,
):
    """Функция изменения статуса проекта при обновлении требуемой суммы для проекта."""
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
        session.add(project)
        await session.commit()


async def invest_in_project(
        project: CharityProject,
        session: AsyncSession,
):
    """Функция распределения свободных сумм пожертвований в новый проект."""
    not_invested_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        )
    )
    not_invested_donations = not_invested_donations.scalars().all()
    await investment_process(project, not_invested_donations, session)


async def investment_process(
        obj_in,
        not_invested_obj_list,
        session: AsyncSession,
):
    """Общая функция инвестирования для пожертвований и проектов."""
    for obj in not_invested_obj_list:
        if not obj_in.fully_invested:
            if obj is not None:
                obj_in_balance = obj_in.full_amount - obj_in.invested_amount
                obj_balance = obj.full_amount - obj.invested_amount
                if obj_in_balance <= obj_balance:
                    obj.invested_amount = obj.invested_amount + obj_in_balance
                    obj_in.invested_amount = obj_in.invested_amount + obj_in_balance
                    obj_in.fully_invested = True
                    obj_in.close_date = datetime.now()
                    if obj_balance == obj_in_balance:
                        obj.fully_invested = True
                        obj.close_date = datetime.now()
                elif obj_in_balance > obj_balance:
                    obj.invested_amount = obj.full_amount
                    obj.fully_invested = True
                    obj.close_date = datetime.now()
                    obj_in.invested_amount = obj_in.invested_amount + obj_balance
                session.add(obj, obj_in)
    await session.commit()
