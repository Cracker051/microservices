from pydantic import BaseModel
from .hospital_schemas import HospitalSchema


class DepartmentCreateSchema(BaseModel):
    id: int
    name: str
    hospitalId: int


class DepartmentReadSchema(BaseModel):
    id: int
    name: str
    hospital: HospitalSchema
