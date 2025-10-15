from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi import Query
from uuid import UUID


class ReadVigils(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    user_ids: Optional[List[UUID]] = Query(None)
    vigil_ids: Optional[List[UUID]] = Query(None)
