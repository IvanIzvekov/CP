from pydantic import BaseModel, Field
from typing import List, Optional

class PostRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}