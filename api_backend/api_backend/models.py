from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

import orjson
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
    xpaths: Optional[dict]
    is_pagination: Optional[bool] = False
    refresh_interval: Optional[int] = 0
    refresh_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    last_refresh_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class SiteOut(SiteIn):
    pass


class SiteModel(BaseModel):
    id: UUID
    domain: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


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

    @property
    def xpaths_json(self):
        return orjson.dumps(self.xpaths).decode("utf-8")


def convert_site_in(site_in: SiteIn) -> (SiteModel, PageModel):
    site = SiteModel(
        id=site_in.id,
        domain=site_in.url.host,
        create_at=datetime.utcnow(),
    )
    page = PageModel(
        site_id=site_in.id,
        url=site_in.url,
        status=site_in.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_pagination=site_in.is_pagination,
        refresh_interval=site_in.refresh_interval,
        refresh_at=datetime.utcnow(),
        last_refresh_at=datetime.utcnow(),
        xpaths=site_in.xpaths,
    )
    return site, page
