from celery import Celery
from celery.schedules import crontab

import os
import datetime

from requests.models import stream_decode_response_unicode
from dotenv import load_dotenv

load_dotenv()

import requests
from bs4 import BeautifulSoup
import pytesseract
from playwright.sync_api import sync_playwright

app = Celery("attendance", broker="redis://localhost")
app.conf.broker_connection_retry_on_startup = False
app.conf.update(timezone="Asia/Kolkata")

POCKETBASE_URL = os.getenv("POCKETBASE_URL")
ATTENDANCE_PATH = "/api/collections/attendance/records"
ADMIN_PATH = "/api/admins/auth-with-password"
STUDENTS_PATH = "/api/collections/students/records"


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    queue_get_attendance.delay()

    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        queue_get_attendance.s(),
    )


@app.task
def queue_get_attendance():
    # Admin token
    r = requests.post(
        f"{POCKETBASE_URL}{ADMIN_PATH}",
        data={
            "identity": os.getenv("ADMIN_EMAIL"),
            "password": os.getenv("ADMIN_PASSWORD"),
        },
    )
    admin_token = r.json()["token"]

    r = requests.get(
        f"{POCKETBASE_URL}{STUDENTS_PATH}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    students = r.json()["items"]
    for student in students:
        get_attendance.delay(
            str(student["registerNo"]), student["password"], student["id"], admin_token
        )


@app.task
def get_attendance(
    username: str, password: str, student_id: str, admin_token: str
) -> float:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_url = (
            "https://erp.velsuniv.ac.in/velsonline/students/loginManager/youLogin.jsp"
        )
        profile_url = (
            "https://erp.velsuniv.ac.in/velsonline/students/report/studentProfile.jsp"
        )
        page.goto(login_url)

        page.fill('input[name="login"]', username)
        page.fill('input[name="passwd"]', password)

        captcha_image = page.locator("//img[@src='/velsonline/captchas']")
        captcha_image.screenshot(path="captcha.png")
        captcha_text = pytesseract.image_to_string("captcha.png").strip()
        page.fill('input[name="ccode"]', captcha_text)

        page.click("#_save")

        home_url = (
            "https://erp.velsuniv.ac.in/velsonline/students/template/HRDSystem.jsp"
        )
        page.wait_for_url(home_url)

        # Retrieve JSESSIONID
        cookies = page.context.cookies()
        jsessionid = next(
            cookie["value"] for cookie in cookies if cookie["name"] == "JSESSIONID"
        )

        # Fetch student profile information
        headers = {
            "Cookie": f"JSESSIONID={jsessionid}",
            "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "en-GB",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "frame",
            "Referer": "https://erp.velsuniv.ac.in/velsonline/students/template/HRDSystem.jsp",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i",
            "Connection": "keep-alive",
        }

        response = requests.get(profile_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                student_name = (
                    soup.find("td", string="Student Name")
                    .find_next_sibling("td")
                    .b.string.strip()
                )
            except AttributeError:
                student_name = "Unknown"

        # Fetch attendance details
        attendance_url = "https://erp.velsuniv.ac.in/velsonline/students/report/studentSubjectWiseAttendance.jsp"
        response = requests.post(attendance_url, headers=headers)

        percentage = 0.0
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the attendance percentage
            subtotal_row = soup.find("tr", class_="subtotal")
            if subtotal_row:
                percentage_td = subtotal_row.find_all("td", align="right")[3]
                percentage = float(percentage_td.string.strip()[:-1])
            else:
                print("Subtotal row not found.")

            # Extract the end date <td>16/Aug/2024</td>

            period_row = soup.find("tr", class_="subheader1")
            if period_row:
                # The correct end date is the fourth <td> in the row
                end_date_td = period_row.find_all("td")[3]
                end_date = end_date_td.string.strip()
                if end_date.lower() == "to":
                    # If "To" was mistakenly extracted, fetch the next sibling <td>
                    end_date = period_row.find_all("td")[4].string.strip()
            else:
                end_date = "Not Found"
                print("Period row not found.")
        else:
            end_date = "Failed to retrieve"
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

        browser.close()
        append_attendance(percentage, student_id, admin_token)
        return percentage


def append_attendance(percentage: float, student_id: str, admin_token: str):
    r = requests.post(
        f"{POCKETBASE_URL}{ATTENDANCE_PATH}",
        json={"percentage": percentage, "student": student_id, "date": datetime.datetime.today().isoformat()},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    print(r.json())
