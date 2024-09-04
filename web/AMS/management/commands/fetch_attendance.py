# AMS/management/commands/fetch_attendance.py
import pytz
from datetime import datetime
from django.core.management.base import BaseCommand
from AMS.models import Student, Attendance
from AMS.utils import fetch_att

class Command(BaseCommand):
    help = 'Fetch attendance for all registered students'

    def handle(self, *args, **kwargs):
        students = Student.objects.all()

        for student in students:
            # Decrypt the password
            username = student.registerNo
            password = student.get_password()  # Use the method to decrypt the password

            try:
                student_name, percentage, end_date = fetch_att(username, password)
                # Convert end_date string to a date object
                end_date = datetime.strptime(end_date, '%d-%m-%Y').date()

                # Save the attendance data
                attendance = Attendance(
                    student=student,
                    date=end_date,
                    percentage=float(percentage.strip('%'))
                )
                attendance.save()

                self.stdout.write(self.style.SUCCESS(f"Successfully updated attendance for {student_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to fetch attendance for {username}: {str(e)}"))
