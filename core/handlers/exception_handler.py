from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
import logging
from core.exceptions.base import AppException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, AppException):
        logger.exception(exc)
        return Response(
            {"sucess": False, "code": exc.default_code, "message": exc.default_message},
            status=exc.status_code,
        )
    response = drf_exception_handler(exc, context)

    if response is None:
        logger.exception("Unhandled exception")
        return Response(
            {
                "success": False,
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
            },
            status=500,
        )
    return response
