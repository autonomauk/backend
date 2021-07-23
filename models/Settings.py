from pydantic import BaseModel
from pydantic.fields import Field 
from enum import Enum

class PlaylistNamingSchemeEnum(str,Enum):
    MONTHLY = "MONTHLY"

class SettingsFields:
    PlaylistNamingScheme = Field(default=PlaylistNamingSchemeEnum.MONTHLY,description="The playlist naming scheme")

    enabled = Field(default=True,description="Enable or disable SpotiCron")

class Settings(BaseModel):
    class Config:
        use_enum_values= True

    PlaylistNamingScheme: PlaylistNamingSchemeEnum = SettingsFields.PlaylistNamingScheme 

    enabled: bool = SettingsFields.enabled