from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from django.utils.translation import gettext as _
from rest_users.utils.api import _build_initial_user

User = auth.get_user_model()


class LoginUserSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def get_authenticated_user(self):
        login, password = self.validated_data['login'], self.validated_data['password']
        user = None
        login_field_names = [User.USERNAME_FIELD, User.EMAIL_FIELD]

        for field_name in login_field_names:
            kwargs = {
                field_name: login,
                'password': password,
            }
            user = auth.authenticate(**kwargs)
            if user:
                break

        return user


class LogoutSerializer(serializers.Serializer):
    revoke_token = serializers.BooleanField(default=False)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, password):
        user = _build_initial_user(self.initial_data)
        validate_password(password, user=user)
        return password

    def get_fields(self):
        fields = super().get_fields()
        fields['password_confirm'] = serializers.CharField(write_only=True)
        return fields

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise ValidationError(_("Passwords don't match"))
        return attrs

    def create(self, validated_data):
        data = validated_data.copy()
        del data['password_confirm']
        return self.Meta.model.objects.create_user(**data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError(_("Old password is not correct"))
        return old_password

    def validate_password(self, password):
        user = self.context['request'].user
        validate_password(password, user=user)
        return password

    def get_fields(self):
        fields = super().get_fields()
        fields['password_confirm'] = serializers.CharField()
        return fields

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(_("Passwords don't match"))
        return attrs

