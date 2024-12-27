from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate, CharityProjectDb, CharityProjectDbforSuperUser
from app.api.validators import check_full_amount, check_unique_name_project, check_unique_name_project_update, check_fully_invested_for_update, check_description_by_create_project, check_charity_project_exists, check_fully_invested_and_invested_amount_for_delete
from app.services.investing import investing_after_create_project

router = APIRouter(prefix='/charity_project', tags=['Charity_Project'])


@router.post(
    '/',
    response_model=CharityProjectDbforSuperUser,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Создание проектов доступно только суперюзерам'''
    await check_unique_name_project(session=session, project_name=charity_project.name)
    await check_description_by_create_project(description=charity_project.description)
    charity_project_db = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )
    await investing_after_create_project(current_project=charity_project_db, session=session)
    await session.commit()
    await session.refresh(charity_project_db)
    return charity_project_db


@router.get(
    '/',
    response_model=List[CharityProjectDb],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDb]:
    charity_projects = await charity_project_crud.get_multi(session=session)
    return charity_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDbforSuperUser,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDbforSuperUser:
    '''Удаление проектов доступно только суперюзерам'''
#    await check_fully_invested_for_update(session=session, project_id=charity_project_id)
    to_delete = await check_fully_invested_and_invested_amount_for_delete(session=session, project_id=charity_project_id)
    charity_project_db = await charity_project_crud.remove(db_obj=to_delete, session=session)
    return charity_project_db


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDbforSuperUser,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDbforSuperUser:
    '''Обновление проектов доступно только суперюзерам.'''
    await check_fully_invested_for_update(session=session, project_id=charity_project_id)
    await check_unique_name_project_update(session=session, project_name=obj_in.name, project_id=charity_project_id)
    obj_db = await check_full_amount(session=session, project_id=charity_project_id, obj_in=obj_in)
    updated_obj = await charity_project_crud.update(
        db_obj=obj_db, obj_in=obj_in, session=session
    )
    return updated_obj
