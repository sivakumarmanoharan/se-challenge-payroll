import io
import os
from datetime import datetime, timezone
import pandas as pd
from fastapi import File

from sqlalchemy import Date, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import WaveChallengeException
from app.models.time_entries import TimeReport, JobGroup, Employee, TimeEntry


class WaveChallengeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_record_there(self, record_number):
        query = select(TimeReport.time_report_id).where(TimeReport.time_report_id == record_number)
        result = await self.session.execute(query)
        result = result.scalars().all()
        is_record_present = False
        if len(result) > 1:
            is_record_present = True
        return is_record_present

    async def upload_file_in_db(self, csv_file: File, record_number):
        # new_time_report = TimeReport(
        #     time_report_id=record_number,
        #     date_uploaded=datetime.now(timezone.utc).date()
        # )
        # self.session.add(new_time_report)
        file_stream = io.TextIOWrapper(csv_file.file, encoding="UTF-8")
        record_dataframe = pd.read_csv(file_stream)
        return record_dataframe
