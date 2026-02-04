from rest_framework.exceptions import APIException
from rest_framework import status


class AppException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "APPLICATION ERROR"
    default_detail = "Unexpected application error"
