from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database.engine import Base


class TimeReport(Base):
    __tablename__ = "time_reports"
    id = Column(Integer, primary_key=True)


class TimeEntry(Base):
    __tablename__ = "time_entries"
    id = Column(UUID, primary_key=True)
    date = Column(Date)
    hours = Column(Integer)
    employee_id = Column(String)
    job_group = Column(String)
    report_id = Column(Integer, ForeignKey('time_reports.id'))
