from repositories.user import UserRepository
from models.ObjectId import PydanticObjectId
from repositories.stats import StatsRepository
from repositories.auth_flow import AuthFlowRepository
from repositories.exceptions import AuthenticationFailureException, UserNotFoundException
from fastapi import APIRouter, Depends
from loguru import logger

from routers.me import settings
from routers.me import track_log

router = APIRouter(
    prefix='/me',
    tags=['me'],
    responses={
        **AuthenticationFailureException.response_model(),
        **UserNotFoundException.response_model()},
)

@router.delete('/')
def delete_user(str = Depends(AuthFlowRepository.auth_required_dep)) -> str:
    UserRepository.delete(PydanticObjectId.validate(id))
    logger.info(f'User with {id=} was deleted')
    StatsRepository.user_deletion()
    return "OK"

router.include_router(settings.router)
router.include_router(track_log.router)