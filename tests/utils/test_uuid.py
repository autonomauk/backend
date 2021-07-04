from bson.objectid import ObjectId
from utils.uuid import get_uuid
from models.ObjectId import PydanticObjectId

def test_get_uuid():
    uuid: PydanticObjectId = get_uuid()

    assert uuid is not None
    assert isinstance(uuid, ObjectId)
    assert PydanticObjectId.is_valid(uuid)
