import pytest
from django.urls import reverse
from factory import Factory
from faker import Faker
from rest_framework import status

from appointment.models import Availability, TimeSlot

fake = Faker()


@pytest.mark.django_db
class TestAvailabilityView:
    def test_patient_create(self, api_client_auth, create_patient):
        """
        patient should not be able to create availability
        """
        patient = create_patient()
        client = api_client_auth(patient.user)

        url = reverse("appointment:availability")
        data = {}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_doctor_create(self, api_client_auth, create_doctor):
        """
        doctor should be able to create availability
        """
        doctor = create_doctor()
        client = api_client_auth(doctor.user)
        url = reverse("appointment:availability")

        slot = TimeSlot.objects.first()
        data = {"doctor": doctor.id, "slot": slot.id, "date": fake.date()}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        # check db
        assert Availability.objects.filter(doctor=doctor).exists()

    def test_patient_list(
        self,
        api_client_auth,
        create_patient,
        availability_factory: Factory,
        create_doctor,
    ):
        """
        patient should be list all availabilities
        """
        patient = create_patient()
        doctor1 = create_doctor()
        doctor2 = create_doctor()

        _ = availability_factory.create_batch(3, **{"doctor": doctor1})
        _ = availability_factory.create_batch(3, **{"doctor": doctor2})

        client = api_client_auth(patient.user)
        url = reverse("appointment:availability")
        response = client.get(url, format="json")
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == 6

    def test_doctor_list(
        self, api_client_auth, availability_factory: Factory, create_doctor
    ):
        """
        doctor should be list only their availabilities
        """
        doctor1 = create_doctor()
        doctor2 = create_doctor()

        _ = availability_factory.create_batch(3, **{"doctor": doctor1})
        _ = availability_factory.create_batch(3, **{"doctor": doctor2})

        client = api_client_auth(doctor1.user)
        url = reverse("appointment:availability")
        response = client.get(url, format="json")
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == 3
