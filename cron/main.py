from celery import Celery
from celery.schedules import crontab

import requests
from bs4 import BeautifulSoup
import pytesseract
from playwright.sync_api import sync_playwright

app = Celery('attendance', broker='redis://localhost')
app.conf.broker_connection_retry_on_startup = False
app.conf.update(timezone = 'Asia/Kolkata')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(1.0, test.s('hello'), name='add every 10')

    # Executes every Monday morning at 7:30 a.m.
    #sender.add_periodic_task(
    #    crontab(hour=7, minute=30, day_of_week=1),
    #    test.s('Happy Mondays!'),
    #)

@app.task
def get_attendance(username: str, password: str) -> float:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open the login page
        login_url = (
            "https://erp.velsuniv.ac.in/velsonline/students/loginManager/youLogin.jsp"
        )
        profile_url = (
            "https://erp.velsuniv.ac.in/velsonline/students/report/studentProfile.jsp"
        )
        page.goto(login_url)

        # Wait for and fill the login form
        page.fill('input[name="login"]', username)
        page.fill('input[name="passwd"]', pwd)

        # Handle CAPTCHA
        captcha_image = page.locator("//img[@src='/velsonline/captchas']")
        captcha_image.screenshot(path="captcha.png")
        captcha_text = pytesseract.image_to_string("captcha.png").strip()
        page.fill('input[name="ccode"]', captcha_text)

        # Submit the login form
        page.click("#_save")

        # Wait for the home page to load
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

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the attendance percentage
            subtotal_row = soup.find("tr", class_="subtotal")
            if subtotal_row:
                percentage_td = subtotal_row.find_all("td", align="right")[3]
                percentage = percentage_td.string.strip()
            else:
                percentage = "Not Found"
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
            percentage = "Failed to retrieve"
            end_date = "Failed to retrieve"
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

        browser.close()
