from http import HTTPStatus

from fastapi import HTTPException


class WaveChallengeException(HTTPException):

    def __init__(self, message, status_code):
        super().__init__(message, status_code)

    @classmethod
    def same_file_upload(cls, message):
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED, detail=message)

    @classmethod
    def internal_server_error(cls, message: str):
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=message)

    @classmethod
    def bad_request(cls, message):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=message)

    @classmethod
    def not_found(cls, message):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=message)
