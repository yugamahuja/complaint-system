import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers.complaints import router as complaints_router
from .routers.dashboard import router as dashboard_router
from .routers.directory import router as directory_router


app = FastAPI(
    title="Customer Complaint Management API",
    description="Initial API foundation for the complaint management system.",
    version="0.1.0",
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = list({frontend_url, "http://localhost:3000", "http://127.0.0.1:3000"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(complaints_router)
app.include_router(dashboard_router)
app.include_router(directory_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
