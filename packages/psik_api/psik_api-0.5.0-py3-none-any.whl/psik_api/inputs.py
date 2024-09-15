import logging
_logger = logging.getLogger(__name__)

from anyio import Path as aPath
from fastapi import APIRouter, HTTPException

import psik

from .config import managers
from .models import ErrorStatus, stamp_re

inputs = APIRouter()

@inputs.post("/{machine}")
async def new_input(machine : str) -> str:
    "Create a new job input directory."

    try:
        mgr = managers[machine]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")

    base = "/error"
    if not await aPath(base).is_dir():
        return ErrorStatus.ERROR
    return ErrorStatus.OK
