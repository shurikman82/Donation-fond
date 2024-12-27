from datetime import datetime as dt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation



async def investing_after_create_project(session: AsyncSession, current_project: CharityProject):
    free_donations = await session.execute(select(Donation).where(Donation.fully_invested == 0))
    donations: list[Donation] = free_donations.scalars().all()
    for donation in donations:
        project__need_money = current_project.full_amount - current_project.invested_amount
        donation_free_money = donation.full_amount - donation.invested_amount
        if donation_free_money >= project__need_money:
            current_project.invested_amount += project__need_money
            current_project.fully_invested = True
            current_project.close_date = dt.now()
            donation.invested_amount += project__need_money
            if donation.full_amount == donation.invested_amount:
                donation.fully_invested = True
                donation.close_date = dt.now()
            return
        else:
            current_project.invested_amount += donation_free_money
            donation.invested_amount += donation_free_money
            donation.fully_invested = True
            donation.close_date = dt.now()


async def investing_after_create_donation(session: AsyncSession, current_donation: Donation):
    free_projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested == 0))
    projects: list[CharityProject] = free_projects.scalars().all()
    for project in projects:
        project__need_money = project.full_amount - project.invested_amount
        donation_free_money = current_donation.full_amount - current_donation.invested_amount
        if donation_free_money >= project__need_money:
            project.invested_amount += project__need_money
            project.fully_invested = True
            project.close_date = dt.now()
            current_donation.invested_amount += project__need_money
            if current_donation.full_amount == current_donation.invested_amount:
                current_donation.fully_invested = True
                current_donation.close_date = dt.now()
                return

        else:
            project.invested_amount += donation_free_money
            current_donation.invested_amount += donation_free_money
            current_donation.fully_invested = True
            current_donation.close_date = dt.now()
            return
