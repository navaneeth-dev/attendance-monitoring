from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pytesseract


def fetch_att(username,pwd):
    # Initialize WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Open the login page
    login_url = 'https://erp.velsuniv.ac.in/velsonline/students/loginManager/youLogin.jsp'
    profile_url = 'https://erp.velsuniv.ac.in/velsonline/students/report/studentProfile.jsp'
    driver.get(login_url)

    # Wait for and fill the login form
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'login'))
    )
    username_input.send_keys(username)  # Replace with your username
    password_input = driver.find_element(By.NAME, 'passwd')
    password_input.send_keys(pwd)  # Replace with your password

    # Handle CAPTCHA
    captcha_image = driver.find_element(By.XPATH, "//img[@src='/velsonline/captchas']")
    captcha_image.screenshot('captcha.png')
    captcha_text = pytesseract.image_to_string('captcha.png').strip()
    captcha_input = driver.find_element(By.NAME, 'ccode')
    captcha_input.send_keys(captcha_text)

    # Submit the login form
    login_button = driver.find_element(By.ID, '_save')
    login_button.click()

    # Wait for the home page
    home_url = 'https://erp.velsuniv.ac.in/velsonline/students/template/HRDSystem.jsp'
    WebDriverWait(driver, 10).until(EC.url_to_be(home_url))

    # Retrieve JSESSIONID
    jsessionid = driver.get_cookie('JSESSIONID')['value']

    # Fetch student profile information
    headers = {
        'Cookie': f'JSESSIONID={jsessionid}',
        'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-GB',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'frame',
        'Referer': 'https://erp.velsuniv.ac.in/velsonline/students/template/HRDSystem.jsp',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=0, i',
        'Connection': 'keep-alive'
    }

    response = requests.get(profile_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            student_name = soup.find('td', text='Student Name').find_next_sibling('td').b.string.strip()
        except AttributeError:
            student_name = "Unknown"


    # Fetch attendance details
    attendance_url = 'https://erp.velsuniv.ac.in/velsonline/students/report/studentSubjectWiseAttendance.jsp'
    response = requests.post(attendance_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        subtotal_row = soup.find('tr', class_='subtotal')
        if subtotal_row:
            percentage_td = subtotal_row.find_all('td', align='right')[3]
            percentage = percentage_td.string.strip()
            
        else:
            print("Data not found!")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


    driver.quit()
    return(student_name,percentage)



