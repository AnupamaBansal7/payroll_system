import csv
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services import calculate_net_salary

app = FastAPI(title="Payroll Processing System")

payroll_records_db = []


@app.post("/payroll/upload")
async def upload_payroll(file: UploadFile = File(...)):
    global payroll_records_db

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))

    processed_records = []

    for row in reader:
        emp_id = (row.get("employee_id") or "").strip()

        if not emp_id or "Automated Payroll" in emp_id or not row.get("monthly_salary"):
            continue

        try:
            monthly_salary = float(row.get("monthly_salary", 0) or 0)
            working_days = int(row.get("working_days", 0) or 0)
            present_days = int(row.get("present_days", 0) or 0)
            bonus = float(row.get("bonus", 0) or 0)

        
            net_salary = calculate_net_salary(monthly_salary, working_days, present_days, bonus)

            record = {
                "employee_id": emp_id,
                "name": (row.get("name") or "").strip(),
                "monthly_salary": monthly_salary,
                "working_days": working_days,
                "present_days": present_days,
                "bonus": bonus,
                "net_salary": net_salary
            }
            processed_records.append(record)

        except (ValueError, TypeError):
            continue


    payroll_records_db = processed_records

    return {
        "status": "SUCCESS",
        "total_records": len(processed_records),
        "data": processed_records
    }


@app.get("/payroll/results")
def get_calculated_results():
    """
    Get the calculated net salary records.
    """
    return {
        "total_records": len(payroll_records_db),
        "records": payroll_records_db
    }

