from fastapi import status, HTTPException


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BaseNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND


class BaseBadRequestException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST


class UserNotAuthenticatedException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User is not authenticated.'


class IncorrectCredentialsException(BaseBadRequestException):
    detail = 'Given login or password is invalid.'


class PostNotExistsException(BaseNotFoundException):
    detail = 'Post not exists.'


class UserAlreadyExistsException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with such VK ID is already registered.'


