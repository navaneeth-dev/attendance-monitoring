from flask import Flask, request, jsonify,make_response 
from pwMod import fetch_att

app = Flask(__name__)

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        /* Optional: Additional custom styles */
    </style>
</head>
<body class="bg-gray-100 h-full w-full flex flex-col items-center justify-center text-gray-900 font-sans">
    <h1 class="font-bold">OnlyVels Attendence Api Endpoint</h1>
    <h3>/attendance?username=YourRegNo&password=YourPassword</h3>
</body>
</html>


    '''
    return make_response(html_content)


@app.route('/attendance', methods=['GET'])
def get_attendance():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        student_name, percentage, end_date = fetch_att(username, password)
        return jsonify({'student_name': student_name, 'percentage': percentage, 'Last Updated': end_date})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3001)
