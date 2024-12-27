from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectUpdate


async def check_full_amount(session: AsyncSession, project_id: int, obj_in: CharityProjectUpdate):
    obj_in = obj_in.dict(exclude_unset=True)
    project = await charity_project_crud.get(project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден')
    project_data = jsonable_encoder(project)
    if 'full_amount' in obj_in:
        if project_data['invested_amount'] > obj_in.get('full_amount'):
            raise HTTPException(status_code=400, detail='Недопустимо снижать целевой сбор ниже уже собранной суммы')
    if project_data['fully_invested']:
        raise HTTPException(status_code=400, detail='Проект уже завершен')
    return project


async def check_fully_invested_for_update(session: AsyncSession, project_id: int):
    project = await charity_project_crud.get(project_id, session=session)
    project_data = jsonable_encoder(project)
    if project_data['fully_invested']:
        raise HTTPException(status_code=400, detail='Закрытый проект нельзя редактировать!')

async def check_unique_name_project(session: AsyncSession, project_name: str):
    project = await charity_project_crud.get_by_name(name=project_name, session=session)
    if project:
        raise HTTPException(status_code=400, detail='Проект с таким именем уже существует!')


async def check_unique_name_project_update(session: AsyncSession, project_name: str, project_id: int):
    project = await charity_project_crud.get_by_name(name=project_name, session=session, project_id=project_id)
    if project:
        raise HTTPException(status_code=400, detail='Проект с таким именем уже существует!')
    

async def check_description_by_create_project(description: str):
    if not description:
        raise HTTPException(status_code=422, detail='Описание проекта не может быть пустым')
    

async def check_charity_project_exists(session: AsyncSession, project_id: int):
    project = await charity_project_crud.get(project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден')
    return project

        

async def check_fully_invested_and_invested_amount_for_delete(session: AsyncSession, project_id: int):
    project = await charity_project_crud.get(project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден')
    project_data = jsonable_encoder(project)
    if project_data['fully_invested']:
        raise HTTPException(status_code=400, detail='В проект были внесены средства, не подлежит удалению!')
    if project_data['invested_amount'] != 0:
        raise HTTPException(status_code=400, detail='В проект были внесены средства, не подлежит удалению!')
    return project
