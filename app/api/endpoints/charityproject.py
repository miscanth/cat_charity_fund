from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_invested_before_delete,
    check_name_duplicate, check_amount_update,
    check_project_closed_before_update,
    check_project_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import project_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investions import invest_in_project, invest_update


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового объекта проекта для пожертвований.
    Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    await invest_in_project(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Частично обновляет отдельный проект.
    Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_project_closed_before_update(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_amount_update(obj_in.full_amount, project)

    project = await project_crud.update(
        project, obj_in, session
    )
    await invest_update(project, session)
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаляет проект и возвращает его данные.
    Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_charity_invested_before_delete(project)
    return await project_crud.remove(
        project, session
    )
