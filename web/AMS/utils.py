from playwright.sync_api import sync_playwright
from dateutil import parser
import pytesseract
import time
from datetime import datetime

def fetch_att(username, pwd, max_retries=3):
    for attempt in range(max_retries):
        start_time = time.time()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                ignore_https_errors=True
            )

            # Block images and CSS
            context.route('**/*.{png,jpg,jpeg}', lambda route: route.abort())
            context.route('**/*.css', lambda route: route.abort())

            # Open the login page and perform login
            page = context.new_page()
            login_url = 'http://184.95.52.42/velsonline/students/loginManager/youLogin.jsp'
            page.goto(login_url)

            # Fill the login form
            page.fill('input[name="login"]', username)
            page.fill('input[name="passwd"]', pwd)

            # Handle CAPTCHA
            captcha_image = page.locator("//img[@src='/velsonline/captchas']")
            captcha_image.screenshot(path='captcha.png')
            captcha_text = pytesseract.image_to_string('captcha.png').strip()
            page.fill('input[name="ccode"]', captcha_text)

            # Submit the login form
            page.click('#_save')
            page.wait_for_load_state('networkidle')

            # Check for "Invalid Captcha" error
            if page.locator("td:has-text('Invalid Captcha')").count() > 0:
                page.close()
                continue  # Retry login

            # Navigate to profile page and fetch student name
            profile = context.new_page()
            profile.goto("http://184.95.52.42/velsonline/students/template/PageLeft.jsp")
            profile.wait_for_selector('td.ui-state-highlight.ui-corner-all b')
            student_name = profile.locator('td.ui-state-highlight.ui-corner-all b').inner_text()

            # Navigate to attendance page and fetch percentage and end date
            att_frame = context.new_page()
            att_frame.goto("http://184.95.52.42/velsonline/students/report/studentSubjectWiseAttendance.jsp")
            att_frame.wait_for_selector('#tblSubjectWiseAttendance tr.subtotal td:has-text("%")')
            percentage = att_frame.locator('#tblSubjectWiseAttendance tr.subtotal td:has-text("%")').inner_text()
            end_date = att_frame.locator('#tblSubjectWiseAttendance tr.subheader1 td:nth-child(4)').inner_text()

            # Close pages and browser
            profile.close()
            att_frame.close()
            page.close()
            browser.close()
            
            date_obj = datetime.strptime(end_date, '%d/%b/%Y')
            end_date = date_obj.strftime('%d-%m-%Y')
            

            
            
            
            return student_name, percentage, end_date

    raise Exception("Failed to login after several attempts due to invalid captcha.")

