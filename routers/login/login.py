from repositories.auth_flow import AuthFlowRepository
from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

@router.get("/",
         description="Begin login flow via Spotify")
def user_login() -> RedirectResponse:
    return AuthFlowRepository.login()


@router.get("/callback",
         description="Handles Spotify callback after successful login"
         )
def user_login_callback(code: str) -> RedirectResponse:
    return AuthFlowRepository.login_callback(code)