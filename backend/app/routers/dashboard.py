from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.dashboard import DashboardSummary
from ..services.dashboard import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def read_dashboard_summary(session: Session = Depends(get_db)) -> DashboardSummary:
    return get_dashboard_summary(session)
