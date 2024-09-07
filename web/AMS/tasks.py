from celery import shared_task
from AMS.models import Student, Attendance
from AMS.utils import fetch_att
from datetime import datetime
from celery.utils.log import get_task_logger

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
            student_name, percentage, end_date = fetch_att(username, password)
            # Convert end_date string to a date object
            end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

            # Save the attendance data
            attendance = Attendance(
                student=student, date=end_date, percentage=float(percentage.strip("%"))
            )
            logger.info(f"Success for {student_name}")
            attendance.save()
        except Exception as e:
            logger.error(e)
