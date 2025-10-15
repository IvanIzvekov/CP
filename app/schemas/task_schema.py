from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    text: str
    expected_date: Optional[datetime] = None
    can_be_completed: Optional[bool] = True
    can_be_deleted: Optional[bool] = True

    @field_validator('expected_date', mode='after')
    def check_date(cls, v):
        if v is None:
            return v
        v = v.replace(tzinfo=None, microsecond=0, second=0, minute=0, hour=0)
        today = datetime.today().replace(microsecond=0, second=0, minute=0, hour=0)
        if v < today:
            raise ValueError("expected_date must be today or in the future")
        return v

    @field_validator('can_be_completed', 'can_be_deleted')
    def check_flags(cls, v, info):
        if v and info.data.get('expected_date') is None:
            raise ValueError(f"expected_date must be set if {info.field_name} is True")
        return v


class TaskUpdate(BaseModel):
    text: str
    expected_date: Optional[datetime] = None

    @field_validator('expected_date', mode='after')
    def check_date(cls, v):
        if v is None:
            return v
        v = v.replace(tzinfo=None, microsecond=0, second=0, minute=0, hour=0)
        today = datetime.today().replace(microsecond=0, second=0, minute=0, hour=0)
        if v < today:
            raise ValueError("expected_date must be today or in the future")
        return v

    @field_validator('can_be_completed', 'can_be_deleted')
    def check_flags(cls, v, info):
        if v and info.data.get('expected_date') is None:
            raise ValueError(f"expected_date must be set if {info.field_name} is True")
        return v


class TaskDelete(BaseModel):
    id: UUID