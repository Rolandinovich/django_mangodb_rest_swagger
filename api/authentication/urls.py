from django.urls import path

from api.authentication.views import (RegistrationAPIView, LoginAPIView, )

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('signin/', LoginAPIView.as_view(), name='signin'),
]
