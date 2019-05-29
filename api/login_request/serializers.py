from rest_framework import serializers

from api.core import errorcodes
from api.core import exceptions
from api.login_request.models import LoginRequest


class LoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginRequest
        fields = ('id', 'user', 'message', 'status',)
        read_only_fields = ('id',)
