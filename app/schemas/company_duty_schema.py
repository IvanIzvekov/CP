from pydantic import BaseModel


class CompanyDutyRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
