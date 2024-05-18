import datetime

from django.utils import timezone
from rest_framework import serializers

from appointment.models import Appointment, Availability, TimeSlot, Waitlist


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ("id", "start_time", "end_time")


def represent_availability(instance: Availability):
    return {
        "id": instance.id,
        "date": instance.date,
        "slot": {
            "id": instance.slot.id,
            "start_time": instance.slot.start_time,
            "end_time": instance.slot.end_time,
        },
        "doctor": {
            "id": instance.doctor.id,
            "first_name": instance.doctor.user.first_name,
            "last_name": instance.doctor.user.last_name,
        },
    }


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ("id", "doctor", "date", "slot")
        extra_kwargs = {"doctor": {"read_only": True}}

    def validate_date(self, value: datetime.date):
        """selected date should not be in the past"""
        now = timezone.now()
        if now.date() > value:
            raise serializers.ValidationError(
                dict(msg="selected date cannot be in the past")
            )
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        doctor = request.user.doctor

        date = validated_data.pop("date")
        slot = validated_data.pop("slot")
        av, _ = Availability.objects.get_or_create(
            date=date, slot=slot, doctor=doctor, defaults={**validated_data}
        )
        return av

    def to_representation(self, instance):
        return represent_availability(instance)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "patient", "availability", "is_confirmed")
        extra_kwargs = {
            "is_confirmed": {"read_only": True},
            "patient": {"read_only": True},
        }

    def validate(self, attrs):
        """
        slot on a date should not duplicate
        """
        request = self.context.get("request")
        patient = request.user.patient

        availability = attrs.get("availability")

        av_slot = availability.slot
        av_date = availability.date

        if _ := Appointment.objects.filter(
            patient=patient,
            availability__slot=av_slot,
            availability__date=av_date,
            is_cancelled=False,
        ).exists():
            raise serializers.ValidationError(
                dict(
                    msg=f"already have an appointment for the slot {av_slot} on the {av_date.strftime('%d.%m.%Y')}"
                )
            )

        return super().validate(attrs)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "patient": {
                "id": instance.patient.id,
                "first_name": instance.patient.user.first_name,
                "last_name": instance.patient.user.last_name,
                "dob": instance.patient.dob,
                "gender": instance.patient.gender,
            },
            "availability": represent_availability(instance.availability),
        }

    def create(self, validated_data):
        request = self.context.get("request")
        patient = request.user.patient
        availability = validated_data.pop("availability")
        ap, _ = Appointment.objects.get_or_create(
            availability=availability, patient=patient
        )
        return ap


class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ("id", "doctor", "patient")
        extra_kwargs = {"patient": {"read_only": True}}

    def create(self, validated_data):
        request = self.context.get("request")
        patient = request.user.patient
        waitlist, _ = Waitlist.objects.get_or_create(
            patient=patient, doctor=validated_data["doctor"]
        )
        return waitlist

    def to_representation(self, instance):
        return {
            "patient": {
                "id": instance.patient.id,
                "first_name": instance.patient.user.first_name,
                "last_name": instance.patient.user.last_name,
                "dob": instance.patient.dob,
                "gender": instance.patient.gender,
            },
            "doctor": {
                "id": instance.doctor.id,
                "first_name": instance.doctor.user.first_name,
                "last_name": instance.doctor.user.last_name,
            },
        }
