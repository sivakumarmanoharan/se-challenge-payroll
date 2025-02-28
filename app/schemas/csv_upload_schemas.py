from pydantic import BaseModel
from typing_extensions import List, Optional, T


class EmployeeRecord(BaseModel):
    employee_id: str
    hours_worked: int
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