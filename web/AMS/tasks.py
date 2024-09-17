from celery import shared_task
from AMS.models import Student, Attendance
from AMS.utils import fetch_att
from datetime import datetime
from celery.utils.log import get_task_logger
import requests
import json

logger = get_task_logger(__name__)


@shared_task
def fetch_attendances(name="AMS.fetch_attendances"):
    logger.info("Fetching all attendances")
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

            logger.info(json.dumps(subject_details))

            # Save the attendance data
            attendance = Attendance(
                student=student,
                date=end_date,
                percentage=float(percentage.strip("%")),
                subject_details=subject_details,
            )
            attendance.save()

            logger.info(f"Successfully updated attendance for {student_name}")

            requests.post(
                f"https://ntfy.foss.rizexor.com/{student.ntfy_topic}",
                data=f"{student_name} attendance is {percentage}",
            )
        except Exception as e:
            logger.error(e)
