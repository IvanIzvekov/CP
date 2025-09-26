from typing import List, Literal, Optional

from pydantic import BaseModel

from app.schemas.company_duty_schema import CompanyDutyRead
from app.schemas.post_schema import PostRead
from app.schemas.rank_schema import RankRead

RankEnum = Literal[
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
]
PostEnum = Literal[1, 2, 3, 4, 5, 6, 7]


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    second_name: str
    invocation: str
    rank_id: Optional[RankEnum] = 1
    post_id: Optional[PostEnum] = 1

    model_config = {"from_attributes": True}


class UserRead(BaseModel):
    id: int
    name: str
    surname: str
    second_name: str
    post: Optional[PostRead] = None
    rank: Optional[RankRead] = None
    duties: List[CompanyDutyRead] = []

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str
