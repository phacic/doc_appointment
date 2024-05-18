import factory
from factory.django import DjangoModelFactory

from appointment.models import Appointment, Availability, TimeSlot
from authentication.tests.factories import DoctorFactory, PatientFactory


class TimeSlotFactory(DjangoModelFactory):
    start_time = factory.Faker("time")
    end_time = factory.Faker("time")

    class Meta:
        model = TimeSlot


class AvailabilityFactory(DjangoModelFactory):
    doctor = factory.SubFactory(DoctorFactory)
    slot = factory.SubFactory(TimeSlotFactory)
    date = factory.Faker("future_date")

    class Meta:
        model = Availability


class AppointmentFactory(DjangoModelFactory):
    patient = factory.SubFactory(PatientFactory)
    availability = factory.SubFactory(AvailabilityFactory)

    class Meta:
        model = Appointment
