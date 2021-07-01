from models.ObjectId import PydanticObjectId

def get_uuid() -> str:
    return PydanticObjectId() 