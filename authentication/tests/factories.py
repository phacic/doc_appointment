import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from authentication.const import GenderChoice
from authentication.models import Doctor, Patient

User = get_user_model()


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    username = factory.LazyAttribute(lambda o: o.email)

    class Meta:
        model = User


class DoctorFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Doctor


class PatientFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dob = factory.Faker("date_of_birth")
    gender = factory.Faker("random_element", elements=GenderChoice.to_list())

    class Meta:
        model = Patient
