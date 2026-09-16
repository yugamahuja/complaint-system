from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total: int
    new: int
    in_progress: int
    resolved: int
    overdue: int
    by_status: dict[str, int]
    by_priority: dict[str, int]
