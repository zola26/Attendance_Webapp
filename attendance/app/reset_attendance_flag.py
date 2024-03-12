# myapp/management/commands/reset_attendance_flag.py
from django.core.management.base import BaseCommand
from models import Student
from django.utils import timezone
import pytz

class Command(BaseCommand):
    help = 'Reset attendance_flag for all students at 8:00 AM in East African time zone'

    def handle(self, *args, **kwargs):
        # Get the current time in East African time zone
        current_time = timezone.now().astimezone(pytz.timezone('Africa/Nairobi'))

        # Check if it's 8:00 AM
        if current_time.hour == 8 and current_time.minute == 0:
            # Reset attendance_flag for all students to True
            Student.objects.all().update(attendance_flag=True)
            self.stdout.write(self.style.SUCCESS('Attendance flags reset successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('No action needed.'))
