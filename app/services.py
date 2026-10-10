import csv
import io
from sqlalchemy.orm import Session
from app.models import PayrollRecord


def process_csv_content(file_content: bytes, payroll_month: str, db: Session):
    decoded = file_content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    records = []

    for row in reader:
        emp_id = (row.get("employee_id") or "").strip()

        if not emp_id or "Automated Payroll" in emp_id or not row.get("monthly_salary"):
            continue

        try:
            monthly_salary = float(row.get("monthly_salary", 0) or 0)
            working_days = int(row.get("working_days", 0) or 0)
            present_days = int(row.get("present_days", 0) or 0)
            bonus = float(row.get("bonus", 0) or 0)

            if working_days <= 0 or present_days < 0 or present_days > working_days:
                continue
        except (ValueError, TypeError):
            continue

        net_salary = round((monthly_salary * present_days / working_days) + bonus, 2)

        record = PayrollRecord(
            employee_id=emp_id,
            name=(row.get("name") or "").strip(),
            payroll_month=payroll_month,
            monthly_salary=monthly_salary,
            working_days=working_days,
            present_days=present_days,
            bonus=bonus,
            net_salary=net_salary,
        )
        db.add(record)
        records.append(record)

    db.commit()
    return records
def calculate_net_salary(monthly_salary: float, working_days: int, present_days: int, bonus: float) -> float:
    if working_days <= 0:
        return 0.0
    
    net_salary = (monthly_salary * present_days / working_days) + bonus
    return round(net_salary, 2)

