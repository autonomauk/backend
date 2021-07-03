from pydantic import BaseModel
from pydantic.fields import Field 
from enum import Enum

class PlaylistNamingSchemeEnum(str,Enum):
    MONTHLY = "MONTHLY"

class Settings(BaseModel):
    class Config:
        use_enum_values= True

    PlaylistNamingScheme = Field(default=PlaylistNamingSchemeEnum.MONTHLY,description="The playlist naming scheme")
    