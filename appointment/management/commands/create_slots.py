from django.core.management.base import BaseCommand

from appointment.utils import create_slots


class Command(BaseCommand):
    help = "Creates time slots for appointments"

    def parse_arguments(self, **options):
        """
        Parse command line arguments
        """
        pass

    def handle(self, *args, **options):
        # self.create_slots()
        create_slots()
        self.stdout.write(self.style.SUCCESS("Successfully created time slots"))
