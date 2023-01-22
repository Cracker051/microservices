from fastapi import APIRouter, status, HTTPException
from ormar import exceptions
from models.hospital import Hospital
from schemas.hospital_schemas import HospitalSchema
from typing import List
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
hospital_router = APIRouter()


@hospital_router.get('/', response_model=List[HospitalSchema], status_code=status.HTTP_200_OK)
@cache(expire=300, namespace='hospital')
async def get_hospitals():
    hospitals = await Hospital.objects.exclude_fields('departments').all()
    return hospitals


@hospital_router.get('/{hospital_id}', response_model=HospitalSchema, status_code=status.HTTP_200_OK)
@cache(expire=300, namespace='hospital')
async def get_hospital_by_id(hospital_id: int):
    try:
        hospital = await Hospital.objects.get(pk=hospital_id)
    except exceptions.NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Hospital with id {hospital_id} couldn't be found!")
    return hospital


@hospital_router.post('/', response_model=HospitalSchema, status_code=status.HTTP_200_OK)
async def create_hospital(hospital_to_create: HospitalSchema):
    try:
        hospital = await Hospital.objects.create(name=hospital_to_create.name, city=hospital_to_create.city, address=hospital_to_create.address)
    except exceptions.ModelError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Check if the input is correct!")
    await FastAPICache.clear(namespace='hospital')
    return hospital


@hospital_router.put('/{hospital_id}', response_model=HospitalSchema, status_code=status.HTTP_200_OK)
async def update_hospital(hospital_id: int, hospital: HospitalSchema):
    if hospital_id != hospital.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ID must match!")
    hospital_to_update = await get_hospital_by_id(hospital_id)
    try:
        await hospital_to_update.update(name=hospital.name, city=hospital.city, address=hospital.address)
    except exceptions.ModelError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Check if the input is correct!")
    await FastAPICache.clear(namespace='hospital')
    return hospital


@hospital_router.delete('/{hospital_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hospital(hospital_id: int):
    hospital_to_delete = await get_hospital_by_id(hospital_id)
    await hospital_to_delete.delete()
    await FastAPICache.clear(namespace='hospital')
    return
