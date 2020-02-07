from django.utils.translation import gettext as _

from rest_users.exeptions import NotTokenRequest
from rest_framework.authtoken.models import Token
from django.contrib import auth
User = auth.get_user_model()


def token_user_request_validator(request):
    token_header = request.headers.get('Token', '')
    if not token_header:
        raise NotTokenRequest(_("No Token Request "))
    token_object = Token.objects.filter(key=token_header)
    if not token_object:
        raise NotTokenRequest(_("Token Invalid :("))
    user_id = token_object[0].user_id
    user_list = User.objects.filter(id=user_id)
    if not user_list:
        raise NotTokenRequest(_("User not found"))
    return user_list[0]
