# OnlyVels AMS(Attendance Monitoring System)

### Front-end - Next.js
### Back-end - PocketBase
<hr>


### api.py - endpoint with Name, Attendance Percentage, Last Updated Date.
### selMod.py - Data Scrape using Selenium 
### pwMod.py - Data Scrape using Play Wright 

## How to use
 
#### Step1 - Run the api.py
``` cmd
python api.py
```
Endpoint
```
http://localhost:3001/attendance?username=YourRegNo&password=YourPassword
```
#### Step2 - cd backend   -->  pocketbase serve
```cmd
cd backend
pocketbase serve
```
#### Step3 - cd  ../frontend  --> npm run dev
```cmd
cd frontend
npm run dev
```
#### Step4 - navigate to /login or /register
```
http://localhost:3000/login 
```
or
```
http://localhost:3000/register
```


## How to update with latest attendance data 

#### Step1 - cd TaskScheduling
#### Step2 - Run the app.py (get and post all registered user attendance data to attendance db)
```cmd
cd TaskScheduling
python app.py
```
