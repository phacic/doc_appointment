from django.contrib import admin

from appointment.models import TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time")
