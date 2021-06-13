
from typing import Union
from time import time

def get_time(seconds_precision=True) -> Union[int,float]:
    return time() if not seconds_precision else int(time())