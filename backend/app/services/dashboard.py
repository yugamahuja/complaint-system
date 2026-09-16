from datetime import datetime, timezone

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from ..models import Complaint, Priority, Status


def get_dashboard_summary(session: Session) -> dict:
    counts = dict(
        session.execute(
            select(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status)
        ).all()
    )
    priority_counts = dict(
        session.execute(
            select(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority)
        ).all()
    )
    overdue = session.scalar(
        select(func.count(Complaint.id)).where(
            Complaint.expected_resolution_date < datetime.now(timezone.utc).date(),
            Complaint.status.not_in((Status.RESOLVED, Status.CLOSED)),
        )
    ) or 0
    return {
        "total": session.scalar(select(func.count(Complaint.id))) or 0,
        "new": counts.get(Status.NEW, 0),
        "in_progress": counts.get(Status.IN_PROGRESS, 0),
        "resolved": counts.get(Status.RESOLVED, 0),
        "overdue": overdue,
        "by_status": {
            status.value: counts.get(status, 0)
            for status in Status
        },
        "by_priority": {
            priority.value: priority_counts.get(priority, 0)
            for priority in Priority
        },
    }
