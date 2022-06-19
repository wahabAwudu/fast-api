

from typing import Union
from fastapi import HTTPException, Header, status


class CommonParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

async def verify_app_headers(x_user: str = Header(), x_token:str = Header()):
    app_headers = ["x-user", "x-token"]
    if not x_user in app_headers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-User header invalid")

    if not x_token in app_headers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")
    return True
