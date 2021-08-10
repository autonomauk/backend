from fastapi import APIRouter, Depends
from loguru import logger
import random
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix='/metrics',
    tags=['metrics']
)

@router.get('/', response_class=PlainTextResponse)
def get_ok() -> str:
    return f"autonoma_average_spoticron_run_time {random.random()}"