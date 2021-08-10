from repositories.exceptions import BaseAPIException

from routers import login
from routers import me

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

import config

app = FastAPI(
    title="AutonomaAPI",
#    docs_url=None if config.ENV == "production" else '/docs',
    redoc_url=None if config.ENV == "production" else '/redoc',
    openapi_url=None if config.ENV == "production" else '/openapi.json'
)

app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]) # TODO Change this
app.add_middleware(PrometheusMiddleware, prefix='autonoma_api', app_name='autonoma_api')

@app.exception_handler(BaseAPIException)
def http_exception_handler(request, exc) -> BaseAPIException:
    return exc.response()

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
