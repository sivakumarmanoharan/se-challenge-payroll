from datetime import date

from pydantic import BaseModel
from typing_extensions import List, Optional, T


class EmployeeRecord(BaseModel):
    employee_id: str
    hours_worked: float
    job_group: str
    date: str


class ListRecords(BaseModel):
    records: List[EmployeeRecord]


class ApiResponse(BaseModel):
    message: str
    data: Optional[T] = None
    statusCode: int

    def to_dict(self):
        return {
            "message": self.message,
            "data": self.data.dict() if isinstance(self.data, BaseModel) else self.data,
            "statusCode": self.statusCode
        }


class PayPeriod(BaseModel):
    startDate: date
    endDate: date


class EmployeeReport(BaseModel):
    employeeId: str
    payPeriod: PayPeriod
    amountPaid: str


class PayrollReport(BaseModel):
    employeeReports: List[EmployeeReport]


class PayrollReportResponse(BaseModel):
    payrollReport: PayrollReport


class JobGroups(BaseModel):
    job_group_id: str
    wages: int
