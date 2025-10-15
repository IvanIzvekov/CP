from pydantic import BaseModel
from uuid import UUID


class RankRead(BaseModel):
    id: UUID
    name: str
    short_name: str

    model_config = {"from_attributes": True}
