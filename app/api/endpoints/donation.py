from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import create_donation, read_all_donations_from_db
# get_by_user
from app.services.investions import invest_donation
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationDB, DonationReadDB

router = APIRouter()


@router.post(
        '/',
        response_model=DonationDB,
        response_model_exclude_none=True) #response_model_exclude_defaults, response_model_exclude_unset
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового объекта пожертвования."""
    new_donation = await create_donation(donation, session)
    await invest_donation(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationReadDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех объектов пожертвования.
    Только для суперюзеров."""
    all_donations = await read_all_donations_from_db(session)
    return all_donations


"""@router.get('/my',
            response_model=list[DonationDB],  # dependencies=[Depends(current_user)]
            # Добавляем множество с полями, которые надо исключить из ответа.
            # response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        # В этой зависимости получаем обычного пользователя, а не суперюзера.
        user: User = Depends(current_user)
):
    # Список пожертвований текущего пользователя.
    my_donations = await get_by_user(session, user) #session=session, user=user
    return my_donations"""
