from django.urls import path

from api.apidocs.views import SwaggerSchemaView

urlpatterns = [
    path('', SwaggerSchemaView.as_view(), name='docs'),
]
