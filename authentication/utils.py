from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User: AbstractUser = get_user_model()


def is_doctor(user: User) -> bool:
    return hasattr(user, "doctor")


def is_patient(user: User) -> bool:
    return hasattr(user, "patient")
