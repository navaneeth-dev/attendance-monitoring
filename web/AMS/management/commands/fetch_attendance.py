from datetime import datetime
from django.core.management.base import BaseCommand
from AMS.models import Student, Attendance
from AMS.utils import fetch_att
import requests
import json
import logging


class Command(BaseCommand):
    help = "Fetch attendance for all registered students"

    def handle(self, *args, **kwargs):
        students = Student.objects.all()

        for student in students:
            # Decrypt the password
            username = student.registerNo
            password = student.get_password()  # Use the method to decrypt the password

            try:
                student_name, percentage, end_date, subs, subs_percents = fetch_att(
                    username, password
                )
                # Convert end_date string to a date object
                end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

                subject_details = {}
                for sub, per in zip(subs, subs_percents):
                    subject_details[sub] = float(per[:-2])

                logging.info(json.dumps(subject_details))

                # Save the attendance data
                attendance = Attendance(
                    student=student,
                    date=end_date,
                    percentage=float(percentage.strip("%")),
                    subject_details=subject_details,
                )
                attendance.save()

                logging.info(f"Successfully updated attendance for {student_name}")

                requests.post(
                    f"https://ntfy.foss.rizexor.com/{student.ntfy_topic}",
                    data=f"{student_name} attendance is {percentage}",
                )
            except Exception as e:
                logging.error(f"Failed to fetch attendance for {username}: {str(e)}")
