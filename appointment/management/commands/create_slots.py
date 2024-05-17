from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand

from appointment.models import TimeSlot


class Command(BaseCommand):
    help = "Creates time slots for appointments"

    def parse_arguments(self, **options):
        """
        Parse command line arguments
        """
        pass

    def handle(self, *args, **options):
        self.create_slots()
        self.stdout.write(self.style.SUCCESS("Successfully created time slots"))

    def create_slots(self):
        # from 9 am to 9 pm
        start_time = time(hour=9, minute=0, second=0)
        end_time = time(hour=21, minute=0, second=0)

        row_start_time = start_time
        while row_start_time < end_time:
            row_end_time = self.add_30_minutes(row_start_time)

            # create row
            ts = TimeSlot.objects.get_or_create(
                start_time=row_start_time, end_time=row_end_time
            )
            # self.stdout.write(str(ts))
            self.stdout.write(
                self.style.NOTICE(f"added {row_start_time} - {row_end_time} -- {ts}")
            )
            row_start_time = row_end_time

    def add_30_minutes(self, tm: time):
        full_datetime = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        # Add minutes
        full_datetime += timedelta(minutes=30)
        # Return the new time object
        return full_datetime.time()
