from rest_framework import serializers

from appointment.models import Appointment, Availability, TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ("id", "start_time", "end_time")


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ("id", "doctor", "date", "slot")

    def create(self, validated_data):
        date = validated_data.pop("date")
        slot = validated_data.pop("slot")
        av, _ = Availability.objects.get_or_create(
            date=date, slot=slot, defaults=validated_data
        )
        return av

    def to_representation(self, instance):
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


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "patient", "availability", "is_confirmed")
