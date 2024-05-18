from django.urls import include, path
from rest_framework import routers

from appointment import views

router = routers.DefaultRouter()
app_name = "appointment"

router.register("availability", views.AvailabilityView, basename="availability")
router.register("", views.AppointmentView, basename="book")

urlpatterns = [
    path("time_slots/", views.TimeSlotView.as_view(), name="time_slots"),
    path("", include(router.urls)),
]
