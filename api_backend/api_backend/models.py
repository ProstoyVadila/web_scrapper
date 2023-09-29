from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

import orjson
from pydantic import BaseModel, Field, AnyHttpUrl
import borsh

from api_backend.utils import is_valid_uuid


class ParseStatus(str, Enum):
    PENDING = "pending"
    SCRAPPER_PROCESSING = "scrapper_processing"
    SCRAPPER_DONE = "scrapper_done"
    SCRAPPER_ERROR = "scrapper_error"
    PARSER_PROCESSING = "parser_processing"
    PARSER_SUCCESS = "parser_done"
    PARSER_ERROR = "parser_error"

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

    @property
    def _borsh_schema(self):
        return borsh.schema(
            {
                "id": borsh.types.string,
                "url": borsh.types.string,
                "status": borsh.types.string,
                "xpaths": borsh.types.hashmap(borsh.types.string, borsh.types.string),
                "is_pagination": borsh.types.bool,
                "refresh_interval": borsh.types.u64,
                "refresh_at": borsh.types.string,
                "last_refresh_at": borsh.types.string,
            }
        )


def into_borsh(data: dict) -> bytes:
    schema = borsh.schema(
        {
            "url": borsh.types.string,
            # "status": borsh.types.string,
            # "xpaths": borsh.types.hashmap(borsh.types.string, borsh.types.string),
        }
    )
    return borsh.serialize(schema, data)


class TestSite(BaseModel):
    url: str
    # status: Optional[ParseStatus] = ParseStatus.PENDING
    # xpaths: Optional[dict]

    @property
    def _borsh_schema(self):
        return

    def into_borsh(self) -> bytes:
        return borsh.serialize(self._borsh_schema, self.dict())


class SiteOut(SiteIn):
    pass


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


class SiteModel(BaseModel):
    id: UUID
    domain: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    # pages: Optional[PageModel] = []


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
