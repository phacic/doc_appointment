from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from appointment.models import Appointment, Availability, TimeSlot, Waitlist
from appointment.serializers import (
    AppointmentSerializer,
    AvailabilitySerializer,
    TimeSlotSerializer,
    WaitlistSerializer,
)
from authentication.permissions import IsDoctor, IsPatient
from authentication.utils import is_doctor, is_patient


class TimeSlotView(ListAPIView):
    queryset = TimeSlot.objects.filter(is_active=True).all()
    serializer_class = TimeSlotSerializer


class AvailabilityView(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = AvailabilitySerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["doctor", "slot"]

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

    def get_permissions(self):
        """
        restrict create to doctors
        """
        if self.action in ["create"]:
            self.permission_classes = [IsDoctor]
        return super().get_permissions()


class AppointmentView(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AppointmentSerializer
    filterset_fields = ["is_confirmed", "is_cancelled"]
    search_fields = [
        "availability__doctor__user__first_name",
        "availability__doctor__user__last_name",
        "patient__user__first_name",
        "patient__user__last_name",
    ]

    def get_queryset(self):
        # return for doc
        if is_doctor(self.request.user):
            return (
                Appointment.objects.filter(
                    is_active=True, availability__doctor__user=self.request.user
                )
                .order_by("availability__slot")
                .all()
            )

        if is_patient(self.request.user):
            return (
                Appointment.objects.filter(
                    is_active=True, patient__user=self.request.user
                )
                .order_by("availability__slot")
                .all()
            )

        return (
            Appointment.objects.filter(is_active=True)
            .order_by("availability__slot")
            .all()
        )

    def get_permissions(self):
        """
        restrict create to patient
        """
        if self.action in ["create", "cancel"]:
            self.permission_classes = [IsPatient]
        return super().get_permissions()

    @action(detail=True, methods=["delete"])
    def cancel(self, request, *args, **kwargs):
        appointment = self.get_object()
        appointment.cancel()

        doctor = appointment.availability.doctor

        # look for next in waitlist to fill cancelled availability
        if (
            next_wait := Waitlist.objects.filter(doctor=doctor)
            .order_by("-created_at")
            .first()
        ):
            availability = appointment.availability
            # move to available slot
            Appointment.objects.create(
                patient=next_wait.patient, availability=availability
            )
            # remove from waitlist
            next_wait.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class WaitlistView(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = WaitlistSerializer
    filterset_fields = ["doctor", "patient"]

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [IsPatient]
        return super().get_permissions()

    def get_queryset(self):
        return Waitlist.objects.filter(is_active=True).all()
