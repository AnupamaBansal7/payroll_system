# Payroll Processing System

A simple backend built with FastAPI and Python to process employee payroll CSV files, compute net salaries, and expose endpoints to view calculated results.



## Salary Calculation Formula

Net Salary = (Monthly Salary * Present Days / Working Days) + Bonus

- Values are rounded to 2 decimal places.
- Handles zero working days and invalid numeric rows safely.

## Setup and Running

1. Install required packages:
   pip install -r requirements.txt

2. Start the server from the root directory:
   uvicorn app.main:app --reload

3. Access interactive API documentation:
   http://127.0.0.1:8000/docs

## API Endpoints

- POST /payroll/upload : Uploads CSV, parses rows, calculates net salary, and stores data.
- GET  /payroll/results : Retrieves stored calculated payroll records.

