from pydantic import BaseModel


class PostRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
