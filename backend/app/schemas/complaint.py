from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from ..models.complaint import Priority, Status


class ComplaintCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=150)
    customer_contact: str = Field(min_length=1, max_length=320)
    subject: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    category_id: int = Field(gt=0)
    priority: Priority
    expected_resolution_date: date


class ComplaintUpdate(BaseModel):
    customer_name: str | None = Field(default=None, min_length=1, max_length=150)
    customer_contact: str | None = Field(default=None, min_length=1, max_length=320)
    subject: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1)
    category_id: int | None = Field(default=None, gt=0)
    priority: Priority | None = None
    assigned_employee_id: int | None = Field(default=None, gt=0)
    expected_resolution_date: date | None = None


class ComplaintAssignment(BaseModel):
    employee_id: int = Field(gt=0)
    description: str | None = Field(default=None, min_length=1)


class ComplaintTransition(BaseModel):
    status: Status
    description: str | None = Field(default=None, min_length=1)


class ComplaintActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: int
    action: str
    description: str
    performed_by: int | None
    created_at: datetime


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    customer_contact: str
    subject: str
    description: str
    category_id: int
    priority: Priority
    assigned_employee_id: int | None
    expected_resolution_date: date
    status: Status
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
    closed_at: datetime | None
    category_name: str | None = None
    assigned_employee_name: str | None = None
    activities: list[ComplaintActivityResponse] = []


class ComplaintListResponse(BaseModel):
    items: list[ComplaintResponse]
    page: int
    page_size: int
    total: int


class StatusFilter(str, Enum):
    NEW = Status.NEW.value
    ASSIGNED = Status.ASSIGNED.value
    IN_PROGRESS = Status.IN_PROGRESS.value
    RESOLVED = Status.RESOLVED.value
    CLOSED = Status.CLOSED.value


class PriorityFilter(str, Enum):
    LOW = Priority.LOW.value
    MEDIUM = Priority.MEDIUM.value
    HIGH = Priority.HIGH.value
    CRITICAL = Priority.CRITICAL.value


class SortField(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    EXPECTED_RESOLUTION_DATE = "expected_resolution_date"
    PRIORITY = "priority"
    STATUS = "status"
    CUSTOMER_NAME = "customer_name"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"
