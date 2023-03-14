from typing import Literal

from pydantic import BaseModel


class OutputDataTwitchSchema(BaseModel):
    types: Literal['games', 'streams', 'streamers']

    class Config:
        use_enum_values = True
