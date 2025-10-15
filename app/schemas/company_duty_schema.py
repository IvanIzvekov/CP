from pydantic import BaseModel
from uuid import UUID


class CompanyDutyRead(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}
