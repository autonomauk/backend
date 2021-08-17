from models.music.TrackLog import TrackLogReturnPaginated, TrackLogs
from models.ObjectId import PydanticObjectId
from repositories.user import UserRepository
from repositories.auth_flow import AuthFlowRepository
from fastapi import APIRouter
from fastapi.param_functions import Depends

router = APIRouter(
    prefix='/track_log',
    tags=['track log']
)

@router.get('/',response_model=TrackLogReturnPaginated)
def track_log(id: str = Depends(AuthFlowRepository.auth_required_dep), offset: int = 0, length: int = 5) -> TrackLogReturnPaginated:
    track_log, total = UserRepository.read_track_log(PydanticObjectId(id), offset, length)
    return {"track_log":track_log,"total":total,"offset":offset,"length":len(track_log)}
