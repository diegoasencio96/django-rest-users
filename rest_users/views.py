from django.contrib import auth
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_users.serializers import (
    LoginUserSerializer, LogoutSerializer, UserProfileSerializer, RegisterUserSerializer, ChangePasswordSerializer
)
from rest_users.exeptions import BadRequest
from rest_users.utils.responses import get_ok_response
User = auth.get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def users(request):
    users_ = User.objects.all().values()
    return Response({
        'users': users_
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

    extra_data = user_create_token(request, user)

    return get_ok_response(_("Login successful"), extra_data=extra_data)


def user_create_token(request, user):
    auth.login(request, user)
    extra_data = {}
    token, _ = Token.objects.get_or_create(user=user)
    extra_data['token'] = token.key
    return extra_data


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    serializer = LogoutSerializer(
        data=request.data,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    auth.logout(request)
    if data['revoke_token']:
        try:
            user.auth_token.delete()
        except Token.DoesNotExist:
            raise BadRequest(_("Cannot remove non-existent token"))

    return get_ok_response(_("Logout successful"))


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer_class = UserProfileSerializer
    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = serializer_class(
            instance=request.user,
            data=request.data,
            partial=partial,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        serializer = serializer_class(
            instance=request.user,
            context={'request': request},
        )
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)

    user = request.user
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

