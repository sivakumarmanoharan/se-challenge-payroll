from typing import List
from sqlalchemy import Integer, ForeignKey, String, Date, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.engine import Base
from datetime import datetime,timezone


class JobGroup(Base):
    __tablename__ = 'job_group'

    job_group_id: Mapped[str] = mapped_column(String(2), primary_key=True)  # e.g., 'A' or 'B'
    wages: Mapped[int] = mapped_column(Integer)

    # Relationships
    employees: Mapped[List["Employee"]] = relationship("Employee", back_populates="job_group")
    time_entries: Mapped[List["TimeEntry"]] = relationship("TimeEntry", back_populates="job_group")


class Employee(Base):
    __tablename__ = 'employee'

    employee_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    job_group_id: Mapped[str] = mapped_column(String(2), ForeignKey('job_group.job_group_id'))

    # Relationships
    job_group: Mapped["JobGroup"] = relationship("JobGroup", back_populates="employees")
    time_entries: Mapped[List["TimeEntry"]] = relationship("TimeEntry", back_populates="employee")


class TimeReport(Base):
    __tablename__ = 'time_report'

    time_report_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_uploaded: Mapped[datetime.date] = mapped_column(Date)

    # Relationships
    time_entries: Mapped[List["TimeEntry"]] = relationship("TimeEntry", back_populates="time_report")


class TimeEntry(Base):
    __tablename__ = 'time_entry'

    time_entry_id: Mapped[str] = mapped_column(String, primary_key=True)

    time_report_id: Mapped[int] = mapped_column(Integer, ForeignKey('time_report.time_report_id'))
    employee_id: Mapped[str] = mapped_column(String(100), ForeignKey('employee.employee_id'))
    job_group_id: Mapped[str] = mapped_column(String(2), ForeignKey('job_group.job_group_id'))

    date_worked: Mapped[datetime.date] = mapped_column(Date)
    hours_worked: Mapped[float] = mapped_column(Float)

    # Relationships
    time_report: Mapped["TimeReport"] = relationship("TimeReport", back_populates="time_entries")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="time_entries")
    job_group: Mapped["JobGroup"] = relationship("JobGroup", back_populates="time_entries")

    def to_dict(self):
        return {
            "time_entry_id": self.time_entry_id,
            "time_report_id": self.time_report_id,
            "employee_id": self.employee_id,
            "job_group_id": self.job_group_id,
            "date_worked": self.date_worked if self.date_worked else None,
            "hours_worked": self.hours_worked,
        }
