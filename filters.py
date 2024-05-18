from django_filters import rest_framework as filters

from appointment.models import Appointment


class AppointmentFilter(filters.FilterSet):
    class Meta:
        model = Appointment
