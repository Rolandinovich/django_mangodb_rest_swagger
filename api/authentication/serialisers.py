from rest_framework import serializers
from django.contrib.auth import authenticate

from api.core import errorcodes
from api.authentication.models import User
from api.core.exceptions import MyException


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    def validate_username(self, value):
        model_class = self.Meta.model
        if model_class.objects.filter(username=value).exists():
            raise MyException(**errorcodes.ERR_LOGIN_ALREADY_EXIST)
        if len(value) < 3 or len(value) > 19:
            raise MyException(**errorcodes.ERR_WRONG_LOGIN)
        return value


    class Meta:
        model = User

        fields = ['username', 'password', 'token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise MyException(**errorcodes.ERR_WRONG_LOGIN)
        if password is None:
            raise MyException(**errorcodes.ERR_WRONG_PASSWORD)

        user = authenticate(username=username, password=password)

        if user is None:
            raise MyException(**errorcodes.ERR_WRONG_LOGIN_OR_PASSWRD)

        return {
            'token': user.token
        }
