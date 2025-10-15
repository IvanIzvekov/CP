from typing import List, Literal, Optional

from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    second_name: str
    invocation: str

    model_config = {"from_attributes": True}