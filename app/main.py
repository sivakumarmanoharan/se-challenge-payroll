from fastapi import FastAPI

# from app.routers import uploads, reports

app = FastAPI(title="Payroll API", version="1.0.0")


# Include routers
# app.include_router(uploads.router)
# app.include_router(reports.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
