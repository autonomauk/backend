import pytest
from models.ObjectId import PydanticObjectId

KNOWN_VALID_OBJECTID   = "60e1d30cb0b30f26464d29c4"
KNOWN_INVALID_OBJECTID = "60e1d30cb0b30f26464d29c"

class TestPydanticObjectId:
    def test_validate(self):
        assert PydanticObjectId.validate(KNOWN_VALID_OBJECTID) is not None

        with pytest.raises(ValueError):
            PydanticObjectId.validate(KNOWN_INVALID_OBJECTID)

    def test_creation(self):
        id = PydanticObjectId()
        assert id is not None
        assert len(str(id)) == 24