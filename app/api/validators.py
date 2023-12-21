from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет уникальность полученного имени проекта."""
    project_id = await project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверяет, существует ли запрошенный проект в базе."""
    project = await project_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_amount_update(
        amount_in: int,
        db_project: CharityProject
) -> None:
    """Запрещает установливать требуемую сумму меньше внесённой."""
    if amount_in < db_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя устанавливать требуемую сумму меньше внесённой!'
        )


async def check_project_closed_before_update(
        db_project: CharityProject
) -> None:
    """Запрещает редактировать закрытый проект."""
    if db_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_charity_invested_before_delete(
        db_project: CharityProject
) -> None:
    """Запрещает удалять закрытый или частично инвестированный проект."""
    if db_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
