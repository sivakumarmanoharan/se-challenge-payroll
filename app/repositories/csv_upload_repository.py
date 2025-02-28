import io
import os
from datetime import datetime, timezone
from http.client import HTTPResponse

import pandas as pd
from fastapi import File

from sqlalchemy import Date, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now

from app.exceptions.exceptions import WaveChallengeException
from app.models.time_entries import TimeReport, JobGroup, Employee, TimeEntry
from app.schemas.csv_upload_schemas import EmployeeRecord, ListRecords


class WaveChallengeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_record_there(self, record_number):
        try:
            query = select(TimeReport).where(TimeReport.time_report_id == int(record_number))
            result = await self.session.execute(query)
            result = result.scalars().all()
            is_record_present = False
            if len(result) == 1:
                is_record_present = True
            return is_record_present
        except SQLAlchemyError as e:
            raise WaveChallengeException.internal_server_error(f"Database querying issue:{e}")

    async def upload_file_in_db(self, csv_file: File, record_number):
        try:
            new_time_report = TimeReport(
                time_report_id=int(record_number),
                date_uploaded=datetime.now(timezone.utc).date()
            )
            self.session.add(new_time_report)
            file_stream = io.TextIOWrapper(csv_file.file, encoding="UTF-8")
            record_dataframe = pd.read_csv(file_stream)
            list_employees = []
            for index, row in record_dataframe.iterrows():
                date_str = str(row['date']).strip()
                hours_str = str(row['hours worked']).strip()
                employee_id = str(row['employee id']).strip()
                job_group_id = str(row['job group']).strip()

                try:
                    date_worked = datetime.strptime(date_str, "%d/%m/%Y").date()
                except ValueError as v:
                    raise ValueError("Incorrect date format passed", v)

                try:
                    hours_worked = int(hours_str)
                except ValueError as v:
                    raise ValueError("Incorrect hours format passed", v)

                employee_query = select(Employee).where(Employee.employee_id == employee_id)
                employee = await self.session.execute(employee_query)
                employee = employee.scalars().all()
                if not employee:
                    employee_record = Employee(
                        employee_id=employee_id,
                        job_group_id=job_group_id
                    )
                    self.session.add(employee_record)
                    await self.session.commit()
                time_entry = TimeEntry(
                    time_entry_id=f"{record_number}_{date_str}",
                    time_report_id=int(record_number),
                    employee_id=employee_id,
                    job_group_id=job_group_id,
                    date_worked=date_worked,
                    hours_worked=hours_worked
                )
                self.session.add(time_entry)
                employee_record = EmployeeRecord(
                    job_group=job_group_id,
                    hours_worked=hours_worked,
                    employee_id=employee_id,
                    date=date_str
                )
                list_employees.append(employee_record)
            # Commit all new TimeEntry records.
            await self.session.commit()
            return ListRecords(records=list_employees)

        except SQLAlchemyError as e:
            raise WaveChallengeException.internal_server_error(f"Database querying issue:{e}")
