from models.User import User
from repositories.auth_flow import AuthFlowRepository
from repositories.user import UserRepository
from models.Settings import Settings, PlaylistNamingSchemeEnum

from fastapi import APIRouter
from fastapi.param_functions import Depends

router = APIRouter(
    prefix='/settings',
    tags=['settings']
)

@router.get("/",response_model=Settings)
def read_users_settings(id: str = Depends(AuthFlowRepository.auth_required_dep)) -> Settings:
    user = UserRepository.get(id)
    return user.settings


@router.patch("/naming_scheme",response_model=Settings)
def update_users_settings(new_naming_scheme: PlaylistNamingSchemeEnum, id: str = Depends(AuthFlowRepository.auth_required_dep)) -> Settings:
    user: User = UserRepository.get(id)
    user.settings.PlaylistNamingScheme = new_naming_scheme
    UserRepository.update(user.id, user)
    return user.settings
