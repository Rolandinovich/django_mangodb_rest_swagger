from rest_framework import serializers

from api.authentication.models import User
from api.core import errorcodes
from api.core import exceptions
from api.login_request.models import LoginRequest


class LoginRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    message = serializers.CharField(required=False)

    class Meta:
        model = LoginRequest
        fields = ('id', 'user', 'message', 'status',)
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        if not validated_data['user'].is_manager:
            raise exceptions.MyException(**errorcodes.ERR_HAVENT_RIGHT)
        return super().update(instance, validated_data)


class ChangeUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_manager')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.is_manager = not instance.is_manager
        instance.save()
        return instance
