import pytest
from django.urls import reverse
from factory import Factory
from faker import Faker
from rest_framework import status

from appointment.models import Availability, TimeSlot, Waitlist

fake = Faker()


@pytest.mark.django_db
class TestAvailabilityView:
    def test_patient_create(self, api_client_auth, create_patient) -> None:
        """
        patient should not be able to create availability
        """
        patient = create_patient()
        client = api_client_auth(patient.user)

        url = reverse("appointment:availability-list")
        data = {
            "doctor": fake.random_int(),
            "slot": fake.random_int(),
            "date": fake.date(),
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_doctor_create(self, api_client_auth, create_doctor):
        """
        doctor should be able to create availability
        """
        doctor = create_doctor()
        client = api_client_auth(doctor.user)
        url = reverse("appointment:availability-list")

        slot = TimeSlot.objects.first()
        data = {"slot": slot.id, "date": fake.future_date()}
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
        url = reverse("appointment:availability-list")
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
        url = reverse("appointment:availability-list")
        response = client.get(url, format="json")
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == 3


@pytest.mark.django_db
class TestAppointmentView:
    def test_book_with_doctor(self, api_client_auth, create_doctor):
        """
        doctor should not be able to book appointment
        """
        doctor = create_doctor()
        client = api_client_auth(doctor.user)
        data = {}
        url = reverse("appointment:book-list")
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_book_with_patient(
        self, api_client_auth, create_patient, availability_factory: Factory
    ) -> None:
        """
        patient should be able to book appointment
        """
        patient = create_patient()
        av = availability_factory.create()

        client = api_client_auth(patient.user)
        url = reverse("appointment:book-list")
        data = {
            "availability": av.id,
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_book_duplicate_slot(
        self,
        api_client_auth,
        create_patient,
        create_doctor,
        time_slot_factory: Factory,
        availability_factory: Factory,
        appointment_factory: Factory,
    ) -> None:
        """
        appointment for an existing slot should fail
        """
        patient = create_patient()
        ts = time_slot_factory.create()
        doctor1 = create_doctor()
        doctor2 = create_doctor()

        # two available for the same slots for same day
        date = fake.future_date()
        av1 = availability_factory.create(
            **{"doctor": doctor1, "slot": ts, "date": date}
        )
        av2 = availability_factory.create(
            **{"doctor": doctor2, "slot": ts, "date": date}
        )

        # one existing appointment
        _ = appointment_factory.create(**{"availability": av1, "patient": patient})

        # attempt to create appointment for the second availability
        client = api_client_auth(patient.user)
        url = reverse("appointment:book-list")
        data = {
            "availability": av2.id,
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cancel_appointment(
        self,
        api_client_auth,
        create_patient,
        appointment_factory: Factory,
    ) -> None:
        """patient should be able to cancel appointment"""
        patient = create_patient()
        appointment = appointment_factory.create(**{"patient": patient})
        client = api_client_auth(patient.user)
        url = reverse("appointment:book-cancel", args=[appointment.id])
        response = client.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        appointment.refresh_from_db()
        assert appointment.is_cancelled

    def test_cancel_appointment_with_waitlist(
        self,
        api_client_auth,
        create_patient,
        create_doctor,
        availability_factory: Factory,
        appointment_factory: Factory,
        waitlist_factory: Factory,
    ) -> None:
        patient = create_patient()
        doctor = create_doctor()

        # current patient appointment
        availability = availability_factory.create(**{"doctor": doctor})
        appointment = appointment_factory.create(
            **{"patient": patient, "availability": availability}
        )

        # waitlist (different patient)
        availability1 = availability_factory.create(**{"doctor": doctor})
        _ = appointment_factory.create(**{"availability": availability1})
        _ = waitlist_factory.create(**{"doctor": doctor})

        client = api_client_auth(patient.user)
        url = reverse("appointment:book-cancel", args=[appointment.id])
        response = client.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_search_appointment(
        self,
        api_client_auth,
        user_factory: Factory,
        create_patient,
        create_doctor,
        appointment_factory: Factory,
    ) -> None:
        patient_name = "Bobby"
        patient_user = user_factory.create(**{"first_name": patient_name})
        patient = create_patient(patient_user)

        _ = appointment_factory.create(**{"patient": patient})
        _ = appointment_factory.create_batch(3)

        client = api_client_auth(patient.user)
        url = reverse("appointment:book-list") + f"?search={patient_name}"
        response = client.get(url, format="json")
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data["count"] == 1


@pytest.mark.django_db
class TestWaitlistView:
    def test_create_with_doctor(self, api_client_auth, create_doctor):
        doctor = create_doctor()
        client = api_client_auth(doctor.user)
        url = reverse("appointment:waitlist-list")
        response = client.post(url, data={}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_with_patient(self, api_client_auth, create_patient, create_doctor):
        patient = create_patient()
        doctor = create_doctor()
        client = api_client_auth(patient.user)
        url = reverse("appointment:waitlist-list")
        data = {
            "doctor": doctor.id,
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        # check db
        assert Waitlist.objects.filter(patient=patient).exists()
