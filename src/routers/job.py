from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, Form
from dependencies import get_current_employee, get_current_employer, get_db
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from models import User, Job, Response
from queries import JobRepository, ResponseRepository

router = APIRouter(prefix="/jobs", tags=["jobs"])


# todo(vvnumb): лучше разделить view и use_case-ы. Для тестового задания это оверкилл


@router.post("/")
async def create_new_job_view(
        payload: schemas.JobInSchema = Body(...),
        db: AsyncSession = Depends(get_db),
        employer: User = Depends(get_current_employer)
) -> schemas.JobSchema:
    """Создание вакансии"""
    job_repo = JobRepository()
    job_instance = Job(**payload.dict(exclude_unset=True))
    job_instance.user_id = employer.id
    job = await job_repo.create(db, job_instance)
    return schemas.JobSchema.from_orm(job)


@router.get("/list")
async def get_job_list_view(
        db: AsyncSession = Depends(get_db),
        limit: Optional[int] = Query(10),
        offset: Optional[int] = Query(0)
) -> List[schemas.JobSchema]:
    """Получение списка вакансий с limit-offset пагинацией"""
    job_repo = JobRepository()
    jobs = await job_repo.get_list(db, limit, offset)
    items = [schemas.JobSchema.from_orm(obj) for obj in jobs]
    return items


@router.get("/{job_id}")
async def get_job_by_id_view(
        db: AsyncSession = Depends(get_db),
        job_id: int = Query(...)
) -> Optional[schemas.JobSchema]:
    """Получение вакансии по id, либо 404"""
    job_repo = JobRepository()
    job: Job = await job_repo.get_single(db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return schemas.JobSchema.from_orm(job)


@router.patch("/{job_id}", dependencies=[Depends(get_current_employer)])
async def update_job_view(
        db: AsyncSession = Depends(get_db),
        job_id: int = Query(...),
        payload: schemas.JobUpdateSchema = Body(...),
) -> schemas.JobSchema:
    """Обноваление заданных полей вакансии"""
    job_repo = JobRepository()
    job: Job = await job_repo.get_single(db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    update_fields = payload.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(job, key, value)
    job = await job_repo.update(db, job)
    return schemas.JobSchema.from_orm(job)


@router.delete("/{job_id}", dependencies=[Depends(get_current_employer)])
async def get_job_by_id_view(
        db: AsyncSession = Depends(get_db),
        job_id: int = Query(...)
):
    """Получение вакансии по id, либо 404"""
    job_repo = JobRepository()
    await job_repo.delete(db, id=job_id)
    return dict(status="ok")


@router.post("/respond/{job_id}")
async def make_new_response_view(
        db: AsyncSession = Depends(get_db),
        employee: User = Depends(get_current_employee),
        job_id: int = Query(...),
        comment: Optional[str] = Form(None)
):
    response_repo = ResponseRepository()
    response = Response(
        user_id=employee.id,
        job_id=job_id,
    )

    if comment is not None:
        response.message = comment
    await response_repo.create(db, response)
    return dict(status="ok")


@router.get("/responses/{job_id}", dependencies=[Depends(get_current_employer)])
async def get_responses_view(
        db: AsyncSession = Depends(get_db),
        job_id: int = Query(...),
        limit: Optional[int] = Query(100),
        offset: Optional[int] = Query(0)
) -> List[schemas.ResponseJobSchema]:
    response_repo = ResponseRepository()
    responses_list = await response_repo.get_list(db, limit, offset, Response.job_id == job_id)
    items = [schemas.ResponseJobSchema.from_orm(obj) for obj in responses_list]
    return items
