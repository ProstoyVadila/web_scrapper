from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from utils import is_valid_uuid


class ParseStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"

    def get(self, status: str):
        return self.__members__.get(status.upper())


class Site(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    url: str
    status: Optional[ParseStatus] = ParseStatus.PENDING
    html: Optional[str]
    xpaths: Optional[dict]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    parsed_values: Optional[dict]
