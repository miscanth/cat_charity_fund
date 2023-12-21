from datetime import datetime
from fastapi import HTTPException
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
            CharityProject.fully_invested == False
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
        setattr(project, 'fully_invested', True)
        setattr(project, 'close_date', datetime.now())
        session.add(project)
        await session.commit()


async def invest_in_project(
        project: CharityProject,
        session: AsyncSession,
):
    """Функция распределения свободных сумм пожертвований в новый проект."""
    not_invested_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False
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
        if obj_in.fully_invested == False:
            if obj is not None:
                obj_in_balance = obj_in.full_amount - obj_in.invested_amount
                obj_balance = obj.full_amount - obj.invested_amount
                if obj_in_balance <= obj_balance:
                    setattr(obj, 'invested_amount', (obj.invested_amount + obj_in_balance))
                    setattr(obj_in, 'invested_amount', obj_in.invested_amount + obj_in_balance)
                    setattr(obj_in, 'fully_invested', True)
                    setattr(obj_in, 'close_date', datetime.now())
                    if obj_balance == obj_in_balance:
                        setattr(obj, 'fully_invested', True)
                        setattr(obj, 'close_date', datetime.now())
                elif obj_in_balance > obj_balance:
                    setattr(obj, 'invested_amount', obj.full_amount)
                    setattr(obj, 'fully_invested', True)
                    setattr(obj, 'close_date', datetime.now())
                    setattr(obj_in, 'invested_amount', (obj_in.invested_amount + obj_balance))
                session.add(obj, obj_in)
        else:
            pass
    await session.commit()
