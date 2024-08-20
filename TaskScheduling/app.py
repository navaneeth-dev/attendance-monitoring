import requests
from pocketbase import PocketBase
from datetime import datetime

# Initialize PocketBase client
pb = PocketBase('http://127.0.0.1:8090')  # Replace with your PocketBase server URL

# Function to format the date as required
def format_datetime(date_string):
    try:
        # Parse the date string
        parsed_date = datetime.strptime(date_string, '%d/%b/%Y')
        # Format it as 'YYYY-MM-DD HH:MM:SS'
        return parsed_date.strftime('%Y-%m-%d 12:00:00')
    except ValueError:
        print(f"Date format error for date string: {date_string}")
        return None

# Function to extract numeric value from percentage string
def extract_percentage_value(percentage_string):
    try:
        # Remove '%' and convert to float
        return float(percentage_string.replace('%', ''))
    except ValueError:
        print(f"Error converting percentage string to float: {percentage_string}")
        return None

# Function to update attendance data for all students
def update_attendance():
    print("Starting the attendance update process...")

    try:
        # Fetch all registered users from the 'students' collection
        response = pb.collection('students').get_list(1, 100)  # Fetch first 100 students; adjust as necessary
        students = response.items
        print(f"Fetched {len(students)} students from the database.")

        # Iterate over each student record
        for student in students:
            register_no = getattr(student, 'register_no', None)
            password = getattr(student, 'password', None)

            if not register_no or not password:
                print(f"Missing register_no or password for student record {student.id}")
                continue

            print(f"Processing student with Register No: {register_no}")

            # Call external API to get attendance data
            api_url = f'http://192.168.1.4:3001/attendance?username={register_no}&password={password}'
            print(f"API URL: {api_url}")

            try:
                api_response = requests.get(api_url)
                api_response.raise_for_status()  # Raise an exception for HTTP errors
                api_data = api_response.json()
                
                last_updated = api_data.get('Last Updated')
                _percentage = api_data.get('percentage')
                percentage = extract_percentage_value(_percentage)
                print(percentage)
                
                if last_updated and percentage:
                    formatted_date = format_datetime(last_updated)
                    if formatted_date:
                        # Prepare data for update
                        update_data = {
                            'registerNo':register_no,
                            'date': formatted_date,
                            'percentage': percentage,
                        }
                        try:
                            # Add a new record to the 'attendance' collection
                            record = pb.collection('attendance').create(update_data)
                            print(f"Record added successfully: {record}")
                        except Exception as e:
                            print(f"An error occurred while adding record: {str(e)}")
                else:
                    print(f"Missing 'Last Updated' or 'percentage' in API response for student {register_no}")

            except requests.RequestException as e:
                print(f"An error occurred while fetching data for student {register_no}: {str(e)}")

    except Exception as e:
        print(f"An error occurred during the attendance update process: {str(e)}")

    print("Attendance update process completed.")

# Run the function to update attendance records
if __name__ == "__main__":
    update_attendance()
