from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from appointment.models import Availability, TimeSlot
from appointment.serializers import AvailabilitySerializer, TimeSlotSerializer
from authentication.permissions import IsDoctor
from authentication.utils import is_doctor


class TimeSlotView(ListAPIView):
    queryset = TimeSlot.objects.filter(is_active=True).all()
    serializer_class = TimeSlotSerializer


class AvailabilityView(ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        for doctors, only show their availability
        :return:
        """
        if is_doctor(self.request.user):
            return Availability.objects.filter(
                doctor__user_id=self.request.user.id, is_active=True
            )
        return Availability.objects.filter(is_active=True).order_by("slot").all()

    def create(self, request, *args, **kwargs):
        """
        restrict create to only doctors
        """
        self.permission_classes = (IsDoctor,)
        return super().create(request, *args, **kwargs)
