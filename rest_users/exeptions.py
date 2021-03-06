from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = _("Bad Request")


class NotTokenRequest(APIException):
    status_code = 400
    default_detail = _("Bad Request")


class UserNotFound(APIException):
    status_code = 404
    default_detail = _("User not found")


class InternalServer(APIException):
    status_code = 500
    default_detail = _("Internal server error")
