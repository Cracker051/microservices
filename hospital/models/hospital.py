import ormar
from pydantic import BaseModel
from db import database, metadata


class Hospital(ormar.Model):
    class Meta:
        tablename = "hospital"
        metadata = metadata
        database = database
        extra = ormar.Extra.ignore

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=30)
    city: str = ormar.String(max_length=30)
    address: str = ormar.String(max_length=30)
