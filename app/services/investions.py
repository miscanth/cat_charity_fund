from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.charityproject import get_project_by_id, get_project_id_by_name
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
    for project in not_invested_projects:
        if donation.fully_invested == False:
            if project is not None:
                project_balance = project.full_amount - project.invested_amount
                donation_balance = donation.full_amount - donation.invested_amount
                if donation_balance <= project_balance:
                    setattr(project, 'invested_amount', (project.invested_amount + donation_balance))
                    setattr(donation, 'invested_amount', donation.invested_amount + donation_balance)
                    setattr(donation, 'fully_invested', True)
                    setattr(donation, 'close_date', datetime.now())
                    if donation_balance == project_balance:
                        setattr(project, 'fully_invested', True)
                        setattr(project, 'close_date', datetime.now())
                elif donation_balance > project_balance:
                    setattr(project, 'invested_amount', project.full_amount)
                    setattr(project, 'fully_invested', True)
                    setattr(project, 'close_date', datetime.now())
                    setattr(donation, 'invested_amount', (donation.invested_amount + project_balance))
                session.add(donation, project)
        else:
            pass
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
    for donation in not_invested_donations:
        if project.fully_invested == False:
            if donation is not None:
                project_balance = project.full_amount - project.invested_amount
                donation_balance = donation.full_amount - donation.invested_amount
                if project_balance <= donation_balance:
                    setattr(donation, 'invested_amount', (donation.invested_amount + project_balance))
                    setattr(project, 'invested_amount', project.invested_amount + project_balance)
                    setattr(project, 'fully_invested', True)
                    setattr(project, 'close_date', datetime.now())
                    if donation_balance == project_balance:
                        setattr(donation, 'fully_invested', True)
                        setattr(donation, 'close_date', datetime.now())
                elif project_balance > donation_balance:
                    setattr(donation, 'invested_amount', donation.full_amount)
                    setattr(donation, 'fully_invested', True)
                    setattr(donation, 'close_date', datetime.now())
                    setattr(project, 'invested_amount', (project.invested_amount + donation_balance))
                session.add(donation, project)
        else:
            pass
    await session.commit()


