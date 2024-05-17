from django.db import models

from authentication.models import Doctor, Patient
from core.models import BaseModel


class TimeSlot(BaseModel):
    """
    represent time slot starting from 9 am to 9 pm 30 minutes apart
    """

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class Availability(BaseModel):
    """
    represent doctors availability
    """

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="availabilities"
    )
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.doctor} - {self.slot}"


class Appointment(BaseModel):
    """
    represent patient doctor appointment
    """

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    availability = models.ForeignKey(
        Availability, on_delete=models.CASCADE, related_name="appointments"
    )
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient} - {self.availability}"


class Wishlist(BaseModel):
    """
    represent patient wishlist. for appointment where doctor is already booked
    """

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="wishlists"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="wishlists"
    )

    def __str__(self):
        return f"{self.doctor} - {self.patient}"
