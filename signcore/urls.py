# myapi/urls.py
from django.urls import include, path
from rest_framework import routers

from . import views
from .DB_API import API
from .Sign import Sign

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('ipfs', views.IPFS.as_view()),
    path('file', API.as_view()),
    path('sign', Sign.as_view()),
]
