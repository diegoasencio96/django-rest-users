from django.contrib import auth
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_users.serializers import (
    LoginUserSerializer, LogoutSerializer, UserGetProfileSerializer, UserProfileSerializer, RegisterUserSerializer, ChangePasswordSerializer
)
from rest_users.exeptions import BadRequest
from rest_users.utils.responses import get_ok_response
from rest_users.validators import token_user_request_validator

User = auth.get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def users(request):
    user = token_user_request_validator(request)
    if user.is_superuser:
        users_ = User.objects.all().values()
        return Response({
            'users': users_
        })
    return Response({
        'detail': 'The Token Owner is not Superuser'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer_class = LoginUserSerializer
    serializer = serializer_class(
        data=request.data,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    user = serializer.get_authenticated_user()

    if not user:
        raise BadRequest(_("Login or password invalid."))

    extra_data = {}
    extra_data = user_create_token(request, user, extra_data)
    extra_data = get_user_profile(request, user, extra_data)

    return get_ok_response(_("Login successful"), extra_data=extra_data)


def user_create_token(request, user, extra_data):
    auth.login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    extra_data['token'] = token.key
    return extra_data


def get_user_profile(request, user, extra_data):
    extra_data['profile'] = UserProfileSerializer(
        instance=user,
        context={'request': request},
    ).data
    return extra_data


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    user = token_user_request_validator(request)
    serializer = LogoutSerializer(
        data=request.data,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    auth.logout(request)
    try:
        user.auth_token.delete()
    except Token.DoesNotExist:
        raise BadRequest(_("Cannot remove non-existent token"))

    return get_ok_response(_("Logout successful"))


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([AllowAny])
def profile(request):
    user = token_user_request_validator(request)
    if request.method in ['PUT', 'PATCH']:
        serializer_class = UserProfileSerializer
        partial = request.method == 'PATCH'
        serializer = serializer_class(
            instance=user,
            data=request.data,
            partial=partial,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        serializer_class = UserGetProfileSerializer
        serializer = serializer_class(
            instance=user,
            context={'request': request},
        )
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    user = token_user_request_validator(request)
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    user.set_password(serializer.validated_data['password'])
    user.save()
    return get_ok_response(_("Password changed successfully"))


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer_class = RegisterUserSerializer
    serializer = serializer_class(
        data=request.data,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)

    kwargs = {}

    with transaction.atomic():
        user = serializer.save(**kwargs)
    output_serializer = UserProfileSerializer(
        instance=user,
        context={'request': request},
    )
    user_data = output_serializer.data
    return Response(user_data, status=status.HTTP_201_CREATED)
