import ormar
from db import database, metadata
from typing import Optional
from pydantic import BaseModel
from models.hospital import Hospital


class Department(ormar.Model):
    class Meta:
        tablename = "department"
        metadata = metadata
        database = database
        extra = ormar.Extra.ignore

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=40)
    hospital: Hospital = ormar.ForeignKey(Hospital, nullable=False)
