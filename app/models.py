import enum
import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class PayrollJob(Base):
    __tablename__ = "payroll_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payroll_month = Column(String, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    total_rows = Column(Integer, default=0)
    successful_rows = Column(Integer, default=0)
    failed_rows = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JobError(Base):
    __tablename__ = "job_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("payroll_jobs.id"))
    row_number = Column(Integer)
    employee_id = Column(String)
    error_message = Column(String)

class PayrollRecord(Base):
    __tablename__ = "payroll_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("payroll_jobs.id"))
    employee_id = Column(String, nullable=False)
    name = Column(String)
    payroll_month = Column(String, nullable=False)
    monthly_salary = Column(Float)
    working_days = Column(Integer)
    present_days = Column(Integer)
    bonus = Column(Float)
    net_salary = Column(Float)

    __table_args__ = (
        UniqueConstraint('employee_id', 'payroll_month', name='uix_emp_month'),
    )
