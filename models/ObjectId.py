from bson import ObjectId
from loguru import logger
from pydantic.json import ENCODERS_BY_TYPE

from uuid import UUID

def validate_uuid4(uuid_string):

    """
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code, 
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a 
    # valid uuid4. This is bad for validation purposes.

    return val.hex == uuid_string

class PydanticObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        valid_uuid4 = None
        valid_objectid = None
        # Back port to when we used UUID4
        try:
            UUID(str(v), version=4)
            valid_uuid4 = True
        except ValueError:
            valid_uuid4 = False

        # Current schema
        valid_objectid = ObjectId.is_valid(v)
            
            
        if valid_objectid or valid_uuid4:
            return cls(v)
        else:
            raise ValueError('Invalid objectid')

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            type="string",
            examples= [str(cls()), str(cls())],
        )

ENCODERS_BY_TYPE[PydanticObjectId] = str