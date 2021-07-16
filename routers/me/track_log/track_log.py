from models.music.TrackLog import TrackLogs
from models.music.Track import Tracks
from models.ObjectId import PydanticObjectId
from repositories.user import UserRepository
from repositories.auth_flow import AuthFlowRepository
from fastapi import APIRouter
from fastapi.param_functions import Depends

router = APIRouter(
    prefix='/track_log',
    tags=['track log']
)


@router.get('/',response_model=TrackLogs)
def track_log(id: str = Depends(AuthFlowRepository.auth_required_dep)) -> TrackLogs:
    track_log: TrackLogs = UserRepository.read_track_log(PydanticObjectId(id))
    return track_log