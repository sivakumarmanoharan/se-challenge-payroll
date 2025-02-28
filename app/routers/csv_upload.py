from http import HTTPStatus
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.engine import get_db
from app.exceptions.exceptions import WaveChallengeException
from app.repositories.csv_upload_repository import WaveChallengeRepository
from app.schemas.csv_upload_schemas import ApiResponse
from app.services.csv_upload_service import WaveChallengeService

router = APIRouter()


async def get_timesheet_service(db: AsyncSession = Depends(get_db)):
    repository = WaveChallengeRepository(db)
    return WaveChallengeService(repository)


@router.post('/upload-csv', status_code=HTTPStatus.CREATED)
async def upload_csv(csv_file: UploadFile = File(...),
                     timesheet_service: WaveChallengeService = Depends(get_timesheet_service)):
    try:
        file_name = csv_file.filename
        if not file_name.endswith('.csv'):
            raise WaveChallengeException.bad_request('Wrong file type uploaded')
        else:
            record_number = file_name.split('.')[0].split('-')[-1]
            csv_file_upload = await timesheet_service.upload_csv_file(
                 csv_file, record_number)
            return ApiResponse(statusCode=HTTPStatus.CREATED, data=csv_file_upload, message="Successfully Created")
    except HTTPException as e:
        if e.status_code == 405:
            raise e
        else:
            raise WaveChallengeException.internal_server_error(e.detail)
