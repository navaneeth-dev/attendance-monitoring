from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import StudentRegistrationForm, LoginForm
from .models import Student, Attendance
from .decorators import login_required


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            registerNo = form.cleaned_data["registerNo"]
            password = form.cleaned_data["password"]
            try:
                student = Student.objects.get(registerNo=registerNo)
                if student.get_password() == password:
                    # Store user info in the session
                    request.session["student_id"] = student.id
                    return redirect("dashboard")
                else:
                    form.add_error(None, "Invalid login credentials")
            except Student.DoesNotExist:
                form.add_error(None, "Invalid login credentials")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def dashboard(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("login")

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        student = None

    student_attendance = []
    error_message = None

    if student:
        student_attendance = Attendance.objects.filter(student=student).order_by(
            "-last_run"
        )
    else:
        error_message = "Student record not found."

    subjects_len = len(student_attendance[0].subject_details)
    subjects = set()
    subject_details = []
    for attendance in student_attendance:
        sj = attendance.subject_details
        if sj is None:
            subject_details.append(
                [
                    attendance.date.strftime("%d %b %Y"),
                    *[0 for _ in range(subjects_len)],
                ]
            )
            continue

        subject_details.append(
            [attendance.date.strftime("%d %b %Y"), *list(sj.values())]
        )
        for subject in sj.keys():
            subjects.add(subject)

    print(subject_details)

    context = {
        "student": student,
        "attendance_records": student_attendance,
        "error_message": error_message,
        "subjects": list(subjects),
        "subject_details": subject_details,
    }

    return render(request, "dashboard.html", context)


def logout_view(request):
    request.session.flush()
    return redirect("login")

