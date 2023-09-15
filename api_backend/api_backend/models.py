from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, AnyHttpUrl

from utils import is_valid_uuid


class ParseStatus(str, Enum):
    PENDING = "pending"
    SCRAPPING_SUCCESS = "scrapping_success"
    SCRAPPING_ERROR = "scrapping_error"
    PARSING_SUCCESS = "parsing_success"
    PARSING_ERROR = "parsing_error"

    def get(self, status: str):
        return self.__members__.get(status.upper())


class SiteIn(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    url: AnyHttpUrl
    status: Optional[ParseStatus] = ParseStatus.PENDING
    html: Optional[str]
    xpaths: Optional[dict]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    parsed_values: Optional[dict]


class SiteOut(BaseModel):
    pass


class SiteModel(BaseModel):
    id: UUID
    domain: str
    create_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class PageModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    site_id: UUID
    url: AnyHttpUrl
    status: Optional[ParseStatus] = ParseStatus.PENDING
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_pagination: Optional[bool] = False
    refresh_interval: Optional[int] = 0
    refresh_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    last_refresh_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    xpaths: Optional[dict]
