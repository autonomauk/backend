from loguru import logger

from config import settings
from repositories.exceptions import BaseAPIException

from routers import login
from routers import me

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html,  get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

app = FastAPI(
    title="AutonomaAPI",
    openapi_url = settings.server.openapi_url if settings.server.docs else None,
    docs_url = None,
    redoc_url = None
)

app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]) # TODO Change this
app.add_middleware(PrometheusMiddleware, prefix='autonoma_api', app_name='autonoma_api')

@app.exception_handler(BaseAPIException)
def http_exception_handler(request, exc) -> BaseAPIException:
    return exc.response()

########
# DOCS #
########
if settings.server.docs:
    @app.get("/docs", include_in_schema=False)
    def swagger_html():
        return get_swagger_ui_html(
            openapi_url=settings.server.API_PATH+app.openapi_url,
            title=app.title + " - Swagger UI"
        )
    @app.get("/redoc", include_in_schema=False)
    def redoc_html():
        return get_redoc_html(
            openapi_url=settings.server.API_PATH+app.openapi_url,
            title=app.title + " - ReDoc"
        )



#####################
# LOGIN/LOGOUT FLOW #
#####################

app.include_router(login.router)

########
# USER #
########

app.include_router(me.router)

###########
# METRICS #
############

app.add_route("/metrics", handle_metrics)

########
# Home #
########

@app.get("/")
def root():
    return RedirectResponse("/")
