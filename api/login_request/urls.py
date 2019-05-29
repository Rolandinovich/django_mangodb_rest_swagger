from rest_framework.routers import DefaultRouter

from api.login_request.views import LoginRequestView

router = DefaultRouter()

router.register(r'', LoginRequestView, basename='loginrequests')

urlpatterns = router.urls
