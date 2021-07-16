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


@router.get('/',response_model=Tracks)
def track_log(id: str = Depends(AuthFlowRepository.auth_required_dep)) -> Tracks:
    tracks: Tracks = UserRepository.read_track_log(PydanticObjectId(id))
    return tracks