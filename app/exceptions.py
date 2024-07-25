from fastapi import status, HTTPException


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class MultipleResultException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Conflict: got multiple results.'