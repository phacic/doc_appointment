import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status

from authentication.const import GenderChoice
from authentication.models import Doctor, Patient

fake = Faker()
User = get_user_model()


@pytest.mark.django_db
class TestDoctorRegistration:
    def test_register_with_invalid_data(self, api_client):
        url = reverse("authentication:register-doctor")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_with_valid_data(self, api_client, test_password):
        url = reverse("authentication:register-doctor")
        email = fake.email()
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
            "password": test_password,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        # check database
        assert Doctor.objects.filter(user__email=email).count() == 1


@pytest.mark.django_db
class TestPatientRegistration:
    def test_register_with_invalid_data(self, api_client):
        url = reverse("authentication:register-patient")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_with_valid_data(self, api_client, test_password):
        url = reverse("authentication:register-patient")
        email = fake.email()
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
            "password": test_password,
            "dob": fake.date(),
            "gender": fake.random_element(GenderChoice.to_list()),
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        # check database
        assert Patient.objects.filter(user__email=email).count() == 1


@pytest.mark.django_db
class TestLogin:
    def test_login_for_doctor(self, api_client, create_doctor, test_password) -> None:
        doctor = create_doctor()

        url = reverse("authentication:login")
        data = {"username": doctor.user.username, "password": test_password}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_for_patient(
        self,
        api_client,
        create_patient,
        test_password,
    ) -> None:
        patient = create_patient()

        url = reverse("authentication:login")
        data = {"username": patient.user.username, "password": test_password}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
