import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from pytest_factoryboy import register
from rest_framework.test import APIClient

from appointment.tests.factories import (
    AppointmentFactory,
    AvailabilityFactory,
    TimeSlotFactory,
)
from appointment.utils import create_slots as cs
from authentication.models import Doctor
from authentication.tests.factories import DoctorFactory, PatientFactory, UserFactory

User = get_user_model()

# register factories
register(UserFactory)
register(DoctorFactory)
register(PatientFactory)
register(TimeSlotFactory)
register(AvailabilityFactory)
register(AppointmentFactory)


@pytest.fixture
def api_client() -> "APIClient":
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_auth(api_client):
    """
    login user
    """

    def make_auth(user: User):
        api_client.force_authenticate(user=user)
        return api_client

    return make_auth


@pytest.fixture()
def test_password():
    return "something-a-bit-serious"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs) -> AbstractUser:
        kwargs["password"] = test_password
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_doctor(db, create_user, user_factory, doctor_factory):
    def make_doctor(user=None) -> Doctor:
        if not user:
            user_data = user_factory.stub().__dict__
            user = create_user(**user_data)
        return doctor_factory.create(user=user)

    return make_doctor


@pytest.fixture
def create_patient(db, create_user, user_factory, patient_factory):
    def make_patient(user=None) -> Doctor:
        if not user:
            user_data = user_factory.stub().__dict__
            user = create_user(**user_data)
        return patient_factory.create(user=user)

    return make_patient


@pytest.fixture(scope="function", autouse=True)
def create_slots(db):
    cs()
