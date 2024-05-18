from django.urls import include, path
from rest_framework import routers

from appointment import views

router = routers.DefaultRouter()
app_name = "appointment"

urlpatterns = [
    path("time_slots/", views.TimeSlotView.as_view(), name="time_slots"),
    path("availability/", views.AvailabilityView.as_view(), name="availability"),
    path("", include(router.urls)),
]
