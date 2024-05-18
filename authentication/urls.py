from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication import views

router = routers.DefaultRouter()

app_name = "authentication"

urlpatterns = [
    # login
    path("login/", TokenObtainPairView.as_view(), name="login"),
    # register
    path(
        "register-doctor/",
        views.DoctorRegistrationView.as_view(),
        name="register-doctor",
    ),
    path(
        "register-patient/",
        views.PatientRegistrationView.as_view(),
        name="register-patient",
    ),
    # all the other apps
    path("", include(router.urls)),
]
