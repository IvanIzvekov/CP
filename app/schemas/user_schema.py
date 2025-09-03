from pydantic import BaseModel
from typing import List, Optional
from app.schemas.post_schema import PostRead
from app.schemas.rank_schema import RankRead
from app.schemas.company_duty_schema import CompanyDutyRead


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    second_name: str
    post_id: Optional[int] = None
    rank_id: Optional[int] = 1
    duties_ids: Optional[List[int]] = []

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