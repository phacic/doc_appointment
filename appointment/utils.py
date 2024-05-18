from datetime import datetime, time, timedelta
from logging import getLogger

from appointment.models import TimeSlot

logger = getLogger(__name__)


def create_slots():
    # from 9 am to 9 pm
    start_time = time(hour=9, minute=0, second=0)
    end_time = time(hour=21, minute=0, second=0)

    row_start_time = start_time
    while row_start_time < end_time:
        row_end_time = add_30_minutes(row_start_time)

        # create row
        ts = TimeSlot.objects.get_or_create(
            start_time=row_start_time, end_time=row_end_time
        )
        logger.info(f"added {row_start_time} - {row_end_time} -- {ts}")
        row_start_time = row_end_time


def add_30_minutes(tm: time):
    full_datetime = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    # Add minutes
    full_datetime += timedelta(minutes=30)
    # Return the new time object
    return full_datetime.time()
