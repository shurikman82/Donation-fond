from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_by_name(
        self,
        name: str,
        session: AsyncSession,
        project_id: Optional[int] = None,
    ):
        request_obj = select(self.model).where(self.model.name == name)
        if project_id:
            request_obj = request_obj.where(self.model.id != project_id)
        db_obj = await session.execute(request_obj)
        return db_obj.scalars().first()

charity_project_crud = CRUDCharityProject(CharityProject)
