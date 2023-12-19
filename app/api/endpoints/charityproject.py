from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_exists, check_name_duplicate
from app.core.db import get_async_session
from app.crud.charityproject import create_charity_project, delete_project, read_all_projects_from_db, update_project
from app.services.investions import invest_in_project
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter()


@router.post(
        '/',
        response_model=CharityProjectDB,
        response_model_exclude_none=True) #response_model_exclude_defaults, response_model_exclude_unset
async def create_new_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового объекта проекта для пожертвований."""
    await check_name_duplicate(project.name, session)
    new_project = await create_charity_project(project, session)
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
    all_projects = await read_all_projects_from_db(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Частично обновляет отдельный проект."""
    project= await check_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    project = await update_project(
        db_project=project, project_in=obj_in, session=session
    )
    return project


@router.delete(
    '/{meeting_room_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаляет объект и возвращает его данные."""
    project = await check_project_exists(
        project_id, session
    )
    project = await delete_project(
        project, session
    )
    return project

