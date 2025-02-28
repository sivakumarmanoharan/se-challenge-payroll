from fastapi import HTTPException, File

from app.exceptions.exceptions import WaveChallengeException
from app.repositories.csv_upload_repository import WaveChallengeRepository
from app.schemas.csv_upload_schemas import ListRecords


class WaveChallengeService:
    def __init__(self, repository: WaveChallengeRepository):
        self.repository = repository

    async def upload_csv_file(self, csv_file: File, record_number):
        try:
            matching_record_number = await self.repository.is_record_there(record_number)
            if matching_record_number:
                raise WaveChallengeException.same_file_upload("Record already exists")
            upload_csv_file = await self.repository.upload_file_in_db(csv_file, record_number)
            return ListRecords.model_validate(upload_csv_file)
        except HTTPException as e:
            if e.status_code == 405:
                raise e
            else:
                raise WaveChallengeException.internal_server_error(e.detail)
