from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("appointment/", include("appointment.urls")),
]
