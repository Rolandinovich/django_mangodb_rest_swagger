from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.authentication.renderers import (RegistrationJSONRenderer, UserJSONRenderer, )
from api.authentication.serialisers import (RegistrationSerializer, LoginSerializer, )

from api.authentication.schemas import CustomersSchema


class RegistrationAPIView(APIView):
    schema = CustomersSchema()
    permission_classes = (AllowAny,)
    renderer_classes = (RegistrationJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        login = request.data.get('login', '')
        password = request.data.get('password', '')
        user = {'username': login, 'password': password}

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    schema = CustomersSchema()
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        login = request.data.get('login', '')
        password = request.data.get('password', '')
        user = {'username': login, 'password': password}
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
