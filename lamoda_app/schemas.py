from typing import Optional

from pydantic import BaseModel, HttpUrl, validator

from .enums import GenderEnum, SectionEnum


class SectionLimitGenderSchema(BaseModel):
    section: SectionEnum
    gender: GenderEnum
    limit: Optional[int] = 30

    @validator('limit')
    def validate_limit(cls, v):
        if not 1 <= v <= 100:
            raise ValueError("limit should be less than or equal to 100")
        return v

    class Config:
        orm_mode = True


class LamodaUrlSchema(BaseModel):
    url: HttpUrl

    @validator('url')
    def validate_url(cls, v):
        if 'lamoda.by' not in v:
            raise ValueError('Make sure that the url belongs to lamoda')
        return v
