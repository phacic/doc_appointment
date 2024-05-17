from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel

User = get_user_model()


class UserBase(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user

    class Meta:
        abstract = True


class Patient(UserBase):
    """
    represents a patient that books an appointment
    """

    pass


class Doctor(UserBase):
    """
    represents a doctor that can accepts an appointment
    """

    pass
