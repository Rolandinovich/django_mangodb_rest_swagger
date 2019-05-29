from rest_framework.routers import DefaultRouter, SimpleRouter, Route

from api.login_request.views import LoginRequestView, ChangeUserStatus


class ChangeUserStatusRouter(SimpleRouter):
    routes = [
        Route(url=r'^{prefix}/$',
              mapping={'get': 'retrieve',
                       'put': 'update', },
              name='{basename}-detail',
              detail=True,
              initkwargs={'suffix': 'Detail'}),
    ]


user_router = ChangeUserStatusRouter()

router = DefaultRouter()

router.register(r'', LoginRequestView, basename='loginrequests')
user_router.register(r'user', ChangeUserStatus, basename='userchangestatus')

urlpatterns = user_router.urls + router.urls