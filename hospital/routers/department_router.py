from fastapi import APIRouter, status, HTTPException
from ormar import exceptions
from models.department import Department, Hospital
from schemas.department_schemas import DepartmentCreateSchema, DepartmentReadSchema
from typing import List
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
department_router = APIRouter()


@department_router.get('/', response_model=List[DepartmentReadSchema], status_code=status.HTTP_200_OK)
@cache(expire=300, namespace='department')
async def get_departments():
    departments = await Department.objects.select_related('hospital').all()
    return departments


@department_router.get('/{department_id}', response_model=DepartmentReadSchema, status_code=status.HTTP_200_OK)
@cache(expire=300, namespace='department')
async def get_department_by_id(department_id: int):
    try:
        department = await Department.objects.select_related('hospital').get(pk=department_id)
    except exceptions.NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Department with id {department_id} couldn't be found!")
    return department


@department_router.post('/', response_model=Department, status_code=status.HTTP_200_OK)
async def create_department(department_to_create: DepartmentCreateSchema):
    if not await Hospital.objects.filter(id=department_to_create.hospitalId).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hospital with id {department_to_create.hospitalId} couldn't be found!")
    try:
        department_to_create.id = 0
        department = await Department.objects.create(
            id=department_to_create.id, name=department_to_create.name, hospital=department_to_create.hospitalId)
    except exceptions.ModelError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Check if the input is correct!")
    await FastAPICache.clear(namespace="department")
    return department


@department_router.put('/{department_id}', response_model=Department, status_code=status.HTTP_200_OK)
async def create_department(department_id: int, department_to_update: DepartmentCreateSchema):
    if department_id != department_to_update.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ID must match!")
    department = await get_department_by_id(department_id)
    if not await Hospital.objects.filter(id=department_to_update.hospitalId).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hospital with id {department_to_update.hospitalId} couldn't be found!")
    try:
        updated_department = await department.update(name=department_to_update.name, hospital=department_to_update.hospitalId)
    except exceptions.ModelError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Check if the input is correct!")
    await FastAPICache.clear(namespace="department")
    return updated_department


@department_router.delete('/{department_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: int):
    department_to_delete = await get_department_by_id(department_id)
    await department_to_delete.delete()
    await FastAPICache.clear(namespace="department")
    return
