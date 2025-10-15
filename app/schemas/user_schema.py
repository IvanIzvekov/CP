from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    second_name: str
    invocation: str

    model_config = {"from_attributes": True}
