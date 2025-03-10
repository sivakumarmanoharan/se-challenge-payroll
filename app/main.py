from fastapi import FastAPI

# from app.routers import uploads, reports
from app.routers.csv_upload import router as csv_upload_router

app = FastAPI(title="Payroll API", version="1.0.0")


# Include routers
# app.include_router(uploads.router)
# app.include_router(reports.router)
app.include_router(csv_upload_router,
                   tags =["Timesheet"])
@app.get("/health")
async def health_check():
    return {"status": "ok"}
