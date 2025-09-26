from pydantic import BaseModel


class RankRead(BaseModel):
    id: int
    name: str
    short_name: str

    model_config = {"from_attributes": True}
