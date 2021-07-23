from models.ObjectId import PydanticObjectId
from pydantic.errors import PydanticErrorMixin
from models.User import User
from repositories.auth_flow import AuthFlowRepository
from repositories.user import UserRepository
from models.Settings import Settings, PlaylistNamingSchemeEnum, SettingsFields

from fastapi import APIRouter
from fastapi.param_functions import Depends, Header

router = APIRouter(
    prefix='/settings',
    tags=['settings']
)

@router.get("/",response_model=Settings)
def read_users_settings(id: PydanticObjectId = Depends(AuthFlowRepository.auth_required_dep)) -> Settings:
    user = UserRepository.get(id)
    return user.settings


@router.patch("/naming_scheme", response_model = PlaylistNamingSchemeEnum)
def update_naming_scheme_setting(new_naming_scheme: PlaylistNamingSchemeEnum = Header(None), id: PydanticObjectId = Depends(AuthFlowRepository.auth_required_dep)) -> PlaylistNamingSchemeEnum:
    user: User = UserRepository.get(id)
    user.settings.PlaylistNamingScheme = new_naming_scheme
    UserRepository.update(user.id, user)
    return user.settings.PlaylistNamingScheme

@router.patch("/enabled", response_model=bool)
def update_enabled_setting(enabled: bool = Header(None), id: PydanticObjectId = Depends(AuthFlowRepository.auth_required_dep)) -> bool:
    user: User = UserRepository.get(id)
    user.settings.enabled = enabled
    UserRepository.update(user.id, user)
    return user.settings.enabled
