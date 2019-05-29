from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from api.authentication.models import User
from api.core.renderrers import ApiJSONRenderer

from api.core import errorcodes
from api.core import exceptions
from api.login_request.models import LoginRequest
from api.login_request.schemas import LoginRequestSchema, ChangeUserStatusSchema
from api.login_request.serializers import LoginRequestSerializer, ChangeUserStatusSerializer


class LoginRequestView(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ApiJSONRenderer,)
    serializer_class = LoginRequestSerializer
    schema = LoginRequestSchema()

    def get_queryset(self):
        return LoginRequest.objects.all()

    def permission_denied(self, request, message=None):
        if not request.successful_authenticator:
            raise exceptions.MyException(**errorcodes.ERR_WRONG_TOKEN)
        super().permission_denied(request, message=None)


class ChangeUserStatus(UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ApiJSONRenderer,)
    serializer_class = ChangeUserStatusSerializer
    schema = ChangeUserStatusSchema()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.pk)

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

    def permission_denied(self, request, message=None):
        if not request.successful_authenticator:
            raise exceptions.MyException(**errorcodes.ERR_WRONG_TOKEN)
        super().permission_denied(request, message=None)
