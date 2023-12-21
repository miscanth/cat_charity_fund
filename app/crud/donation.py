from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession, user: User,
    ) -> list[Donation]:
        """Возвращает список всех пожертвований в базе для текущего пользователя."""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)

"""async def create_donation(
        new_donation: DonationCreate,
        session: AsyncSession,
) -> Donation:
    #Создание нового объекта пожертвования.
    new_donation_data = new_donation.dict()
    db_donation = Donation(**new_donation_data)
    session.add(db_donation)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation


async def read_all_donations_from_db(
        session: AsyncSession,
) -> list[Donation]:
    # Возвращает список всех пожертвований в базе.
    # Только для суперюзеров.
    db_donations = await session.execute(select(Donation))
    return db_donations.scalars().all()"""


"""async def get_by_user(
            self,
            session: AsyncSession, user: User,
    ) -> list[Donation]:
    # Возвращает список всех пожертвований в базе для текущего пользователя.
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donations = donations.scalars().all()
        return donations"""
