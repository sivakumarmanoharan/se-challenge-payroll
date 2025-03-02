from collections import defaultdict

from fastapi import HTTPException, File

from app.core.utils.utils import get_pay_period
from app.exceptions.exceptions import WaveChallengeException
from app.repositories.csv_upload_repository import WaveChallengeRepository
from app.schemas.csv_upload_schemas import ListRecords, EmployeeReport, PayPeriod, PayrollReport, PayrollReportResponse


class WaveChallengeService:
    def __init__(self, repository: WaveChallengeRepository):
        self.repository = repository

    async def upload_csv_file(self, csv_file: File, record_number):
        try:
            matching_record_number = await self.repository.is_record_there(record_number)
            if matching_record_number:
                return WaveChallengeException.same_file_upload("Record already exists")
            upload_csv_file = await self.repository.upload_file_in_db(csv_file, record_number)
            return ListRecords.model_validate(upload_csv_file)
        except HTTPException as e:
            if e.status_code == 405:
                raise e
            else:
                raise WaveChallengeException.internal_server_error(e.detail)

    async def generate_payroll_service(self):
        try:
            job_group_data = await self.repository.job_group_data()
            time_entry_data = await self.repository.time_entry_data()
            employee_pay_data = defaultdict(lambda: defaultdict(float))
            # Keep track of each employee's job group.
            employee_job_group = {}

            for entry in time_entry_data:
                emp_id = entry["employee_id"]
                job_group_id = entry["job_group_id"]
                date_worked = entry["date_worked"]  # Should be a Python date object
                hours_worked = entry["hours_worked"]

                # Look up the hourly rate for the employee's job group.
                rate = job_group_data.get(job_group_id, 0)
                if rate == 0:
                    raise Exception(f"Rate per hour not configured for job group: {job_group_id}")

                # Determine the pay period for the current time entry.
                period = get_pay_period(date_worked)
                period_key = (period.startDate, period.endDate)
                employee_pay_data[emp_id][period_key] += hours_worked

                # Save the employee's job group (assuming it remains consistent).
                employee_job_group[emp_id] = job_group_id

            # Build a list of EmployeeReport objects, sorted by employee id and pay period start date.
            employee_reports = []
            for emp_id in sorted(employee_pay_data.keys(), key=lambda x: int(x)):
                for (start_date, end_date), total_hours in sorted(
                        employee_pay_data[emp_id].items(), key=lambda item: item[0][0]
                ):
                    rate = job_group_data[employee_job_group[emp_id]]
                    amount_paid = total_hours * rate
                    employee_reports.append(
                        EmployeeReport(
                            employeeId=emp_id,
                            payPeriod=PayPeriod(startDate=start_date, endDate=end_date),
                            amountPaid=f"${amount_paid:.2f}"
                        )
                    )

            # Wrap the list inside the final report structure.
            payroll_report = PayrollReport(employeeReports=employee_reports)
            return PayrollReportResponse(payrollReport=payroll_report)
        except HTTPException as e:
            raise WaveChallengeException.internal_server_error(e.detail)

    async def add_job_group(self, job_group):
        try:
            job_group_addition = await self.repository.add_job_group(job_group)
            return job_group_addition
        except HTTPException as e:
            raise  WaveChallengeException.internal_server_error(e.detail)
