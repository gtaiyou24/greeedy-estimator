from __future__ import annotations

from enum import Enum

from http import HTTPStatus

from slf4py import set_logger


@set_logger
class ErrorLevel(Enum):
    WARN = 'WARN'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    def to_logger(self, error_code: ErrorCode, detail: str):
        msg = "[Code] {code} [Message] {message} [Detail] {detail}".format(
            code=error_code.name, message=error_code.message, detail=detail)
        if self == ErrorLevel.WARN:
            self.log.warning(msg)
        elif self == ErrorLevel.ERROR:
            self.log.error(msg)
        elif self == ErrorLevel.CRITICAL:
            self.log.critical(msg)
        else:
            self.log.info(msg)


class ErrorCode(Enum):
    IMAGE_NOT_FOUND = ('画像が見つかりませんでした。', ErrorLevel.ERROR, HTTPStatus.NOT_FOUND)

    def __init__(self, message: str, error_level: ErrorLevel, http_status: HTTPStatus):
        self.message = message
        self.error_level = error_level
        self.http_status = http_status

    def log(self, detail: str):
        self.error_level.to_logger(self, detail)
