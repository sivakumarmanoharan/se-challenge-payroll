from fastapi import HTTPException, File

from app.exceptions.exceptions import WaveChallengeException
from app.repositories.csv_upload_repository import WaveChallengeRepository


class WaveChallengeService:
    def __init__(self, repository: WaveChallengeRepository):
        self.repository = repository

    async def upload_csv_file(self, csv_file: File, record_number):
        try:
            matching_record_number = await self.repository.is_record_there(record_number)
            if matching_record_number:
                return WaveChallengeException.same_file_upload("Record already exists")
            upload_csv_file = await self.repository.upload_file_in_db(csv_file, record_number)
            return upload_csv_file
        except HTTPException as e:
            return WaveChallengeException.internal_server_error(e.detail)
