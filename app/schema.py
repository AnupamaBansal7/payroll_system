from pydantic import BaseModel
from typing import List


class PayrollRecordSchema(BaseModel):
    employee_id: str
    name: str
    monthly_salary: float
    working_days: int
    present_days: int
    bonus: float
    net_salary: float


class JobResultsResponse(BaseModel):
    total_processed: int
    records: List[PayrollRecordSchema]

