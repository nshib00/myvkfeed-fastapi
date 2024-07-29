from fastapi import status, HTTPException


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''
    headers = {}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class BaseNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND


class BaseBadRequestException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST


class BaseUnauthorizedException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {'WWW-Authenticate': 'Bearer'}


class ForbiddenException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Insufficient rights.'


class InvalidTokenException(BaseUnauthorizedException):
    detail = 'Token is invalid.'


class UserNotAuthenticatedException(BaseUnauthorizedException):
    detail = 'User is not authenticated.'


class UserNotActiveException(BaseUnauthorizedException):
    detail = 'User is not active. Please, sign in again.'


class TokenExpiredException(BaseUnauthorizedException):
    detail = 'Token is expired.'


class InvalidTokenDataException(BaseUnauthorizedException):
    detail = 'Token data is invalid.'


class IncorrectCredentialsException(BaseBadRequestException):
    detail = 'Given login or password is invalid.'


class PostNotExistsException(BaseNotFoundException):
    detail = 'Post not exists.'


class UserNotExistsException(BaseNotFoundException):
    detail = 'User with given data not exists.'


class UserAlreadyExistsException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with such VK ID is already registered.'


