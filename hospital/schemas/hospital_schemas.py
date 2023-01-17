from pydantic import BaseModel


class HospitalSchema(BaseModel):
    id: int
    name: str
    city: str
    address: str
