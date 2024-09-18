from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Enum as SQLEnum,
    ForeignKey,
    Boolean,
    Numeric,
    Time,
    JSON,
)
from enum import Enum
from sqlalchemy.orm import relationship
from br_common.models import BaseModel
from br_common.features.sales.models import SalesOffice


# Enum class for the position field
class EmployeePosition(Enum):
    pre_seller = "pre_seller"
    sales_man = "sales_man"
    delivery_driver = "delivery_driver"
    supervisor = "supervisor"


# Enum for Employee Status
class EmployeeStatus(Enum):
    A = "A"  # ACTIVE
    I = "I"  # INACTIVE
    OL = "OL"  # ON_LEAVE


# Enum for Department
class DepartmentEnum(Enum):
    Sales = "Sales"
    Logistics = "Logistics"
    IT = "IT"
    Finance = "Finance"
    HR = "HR"


class HRMaster(BaseModel):
    __tablename__ = "hr_master"

    emp_id = Column(String(10), unique=True, nullable=False)
    status = Column(
        SQLEnum(EmployeeStatus, native_enum=False), nullable=False
    )  # Employee Status (A = Active, I = Inactive, OL = On Leave)
    name_eng = Column(String(255), nullable=False)  # Employee Name (English)
    name_arb = Column(String(255), nullable=False)  # Employee Name (Arabic)
    email = Column(String(255), nullable=False, unique=True)
    mobile_number = Column(String(20), nullable=False, unique=True)
    position = Column(SQLEnum(EmployeePosition, native_enum=False), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    personal_subarea = Column(String(100), nullable=False)

    private_license = Column(String(50), nullable=True)
    private_license_expiry = Column(Date, nullable=True)

    govt_id = Column(String(50), nullable=False)
    nationality = Column(String(100), nullable=False)
    iqama_issuance_number = Column(String(50), nullable=True)
    basic_salary = Column(
        Numeric(10, 2), nullable=True
    )  # Basic Salary should be Masked

    shift_rule = Column(String(100), nullable=True)
    shift_start_time = Column(Time, nullable=True)
    shift_end_time = Column(Time, nullable=True)

    required_working_hours = Column(Numeric(5, 2), nullable=True)
    required_working_days = Column(Numeric(3), nullable=True)

    company_code = Column(String(20), nullable=False)
    department = Column(SQLEnum(DepartmentEnum), nullable=False)
    sales_office_id = Column(Integer, ForeignKey("sales_offices.id"), nullable=False)
    supervisor_id = Column(
        String(10), ForeignKey("hr_master.emp_id"), nullable=True
    )  # Supervisor ID (Self-referencing FK for parent-child relation)

    temporary_block = Column(Boolean, default=False)

    # Relationships for Foreign Key fields
    supervisor = relationship("HRMaster", remote_side=[emp_id], backref="subordinates")
    sales_office = relationship("SalesOffice", backref="employees")

    def __repr__(self):
        return f"<HRMaster: {[self.name_eng if self.name_eng else 'Unsaved']}"


class EmployeeAuditLog(BaseModel):
    __tablename__ = "employee_audit_logs"

    emp_id = Column(String(10), ForeignKey("hr_master.emp_id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    context = Column(
        JSON, nullable=False
    )  # Stores additional event details in JSON format
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    employee = relationship("HRMaster", backref="audits")

    def __repr__(self):
        return f"<EmployeeAuditLog: {[self.id if self.id else 'Unsaved']}"

    @classmethod
    def create(cls, db, emp_id, event_type, context, latitude=None, longitude=None):
        instance = cls(
            emp_id=emp_id,
            event_type=event_type,
            context=context,
            latitude=latitude,
            longitude=longitude,
        )
        instance.save(db)
        return instance
