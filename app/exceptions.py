from fastapi import status, HTTPException


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BaseNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND


class PostNotExistsException(BaseNotFoundException):
    detail = 'Post not exists.'


class MultipleResultException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Conflict: got multiple results.'


