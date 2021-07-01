from utils import get_time
import datetime
from pydantic import BaseModel, Field

class TimedBaseModel(BaseModel):
    createdAt: datetime.datetime= Field(
        description="Created at datetime",
        default_factory=lambda: get_time()
    )

    updatedAt: datetime.datetime = Field(
        description="Created at datetime",
        default_factory=lambda: get_time()
    )
