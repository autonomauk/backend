from bson import ObjectId
import bson
from pydantic.json import ENCODERS_BY_TYPE

class PydanticObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            ObjectId.is_valid(v)
            return cls(v)
        except bson.errors.InvalidId:
            raise ValueError(f"Invalid value {v} for {type(PydanticObjectId)}")


    @classmethod
    def __modify_schema__(cls, field_schema: dict): # pragma: no cover
        field_schema.update(
            type="string",
            examples= [str(cls()), str(cls())],
        )

# Allow JSON encoding as string
ENCODERS_BY_TYPE[PydanticObjectId] = str