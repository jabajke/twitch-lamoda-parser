from typing import Optional

from pydantic import BaseModel, ValidationError, validator

from .enums import GenderEnum, SectionEnum


class SectionLimitGenderSchema(BaseModel):
    section: SectionEnum
    gender: GenderEnum
    limit: Optional[int] = 30

    @validator('limit')
    def validate_limit(cls, v):
        if not 1 <= v <= 100:
            raise ValidationError("limit should be less than or equal to 100")
        return v
