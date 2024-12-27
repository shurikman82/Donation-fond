from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser,current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDb, DonationDBforSuperUser
from app.services.investing import investing_after_create_donation


router = APIRouter(prefix='/donation', tags=['Donation'])

@router.post(
    '/',
    response_model=DonationDb,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationDb:
    new_donation = await donation_crud.create(obj_in=donation, user=user, session=session)
    await investing_after_create_donation(current_donation=new_donation, session=session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDb],
)
async def get_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> List[DonationDb]:
    my_donation = await donation_crud.get_user_donations(user_id=user.id, session=session)
    return my_donation


@router.get(
    '/',
    response_model=List[DonationDBforSuperUser],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationDBforSuperUser]:
    '''Получить список всех пожертвований. Доступно только суперюзерам'''
    all_donations = await donation_crud.get_multi(session=session)
    return all_donations
