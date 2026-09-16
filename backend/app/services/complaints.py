from datetime import datetime, timezone

from sqlalchemy import Select, String, cast, func, or_, select
from sqlalchemy.orm import Session, selectinload

from ..models import (
    Category,
    Complaint,
    ComplaintActivity,
    Employee,
    Priority,
    Status,
)
from ..schemas.complaint import SortField, SortOrder


class ComplaintNotFoundError(Exception):
    pass


class ComplaintValidationError(Exception):
    pass


class ComplaintWorkflowError(Exception):
    pass


def _validate_references(
    session: Session, category_id: int, assigned_employee_id: int | None
) -> None:
    if session.get(Category, category_id) is None:
        raise ComplaintValidationError("category_id does not exist")
    if assigned_employee_id is not None and session.get(Employee, assigned_employee_id) is None:
        raise ComplaintValidationError("assigned_employee_id does not exist")


def create_complaint(session: Session, data) -> Complaint:
    if session.get(Category, data.category_id) is None:
        raise ComplaintValidationError("category_id does not exist")
    complaint = Complaint(
        customer_name=data.customer_name,
        customer_contact=data.customer_contact,
        subject=data.subject,
        description=data.description,
        category_id=data.category_id,
        priority=data.priority,
        expected_resolution_date=data.expected_resolution_date,
        status=Status.NEW,
    )
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    return complaint


def get_complaint(session: Session, complaint_id: int) -> Complaint:
    complaint = session.scalar(
        select(Complaint)
        .options(
            selectinload(Complaint.category),
            selectinload(Complaint.assigned_employee),
            selectinload(Complaint.activities),
        )
        .where(Complaint.id == complaint_id)
    )
    if complaint is None:
        raise ComplaintNotFoundError
    return complaint


def update_complaint(session: Session, complaint_id: int, data) -> Complaint:
    complaint = get_complaint(session, complaint_id)
    values = data.model_dump(exclude_unset=True)
    if values.get("category_id") is None and "category_id" in values:
        raise ComplaintValidationError("category_id cannot be null")
    if "category_id" in values or "assigned_employee_id" in values:
        _validate_references(
            session,
            values.get("category_id", complaint.category_id),
            values.get("assigned_employee_id", complaint.assigned_employee_id),
        )
    for field, value in values.items():
        setattr(complaint, field, value)
    if values:
        changed_fields = ", ".join(values)
        session.add(
            ComplaintActivity(
                complaint=complaint,
                action="UPDATED",
                description=f"Complaint details updated: {changed_fields}.",
                performed_by=complaint.assigned_employee_id,
            )
        )
    session.commit()
    session.refresh(complaint)
    return complaint


def assign_complaint(
    session: Session, complaint_id: int, employee_id: int, description: str | None
) -> Complaint:
    complaint = get_complaint(session, complaint_id)
    if complaint.status != Status.NEW:
        raise ComplaintWorkflowError("Only NEW complaints can be assigned")
    employee = session.get(Employee, employee_id)
    if employee is None:
        raise ComplaintValidationError("assigned employee does not exist")

    complaint.assigned_employee_id = employee_id
    complaint.status = Status.ASSIGNED
    session.add(
        ComplaintActivity(
            complaint=complaint,
            action="ASSIGNED",
            description=description or f"Complaint assigned to {employee.name}.",
            performed_by=employee_id,
        )
    )
    session.commit()
    session.refresh(complaint)
    return complaint


ALLOWED_TRANSITIONS: dict[Status, Status] = {
    Status.NEW: Status.ASSIGNED,
    Status.ASSIGNED: Status.IN_PROGRESS,
    Status.IN_PROGRESS: Status.RESOLVED,
    Status.RESOLVED: Status.CLOSED,
}


def transition_complaint(
    session: Session, complaint_id: int, target_status: Status, description: str | None
) -> Complaint:
    complaint = get_complaint(session, complaint_id)
    expected_status = ALLOWED_TRANSITIONS.get(complaint.status)
    if expected_status != target_status:
        raise ComplaintWorkflowError(
            f"Invalid transition from {complaint.status.value} to {target_status.value}"
        )

    complaint.status = target_status
    now = datetime.now(timezone.utc)
    if target_status == Status.RESOLVED:
        complaint.resolved_at = now
    elif target_status == Status.CLOSED:
        complaint.closed_at = now
    session.add(
        ComplaintActivity(
            complaint=complaint,
            action=target_status.value,
            description=description or f"Complaint moved to {target_status.value}.",
            performed_by=complaint.assigned_employee_id,
        )
    )
    session.commit()
    session.refresh(complaint)
    return complaint


def list_complaints(
    session: Session,
    *,
    search: str | None,
    status: Status | None,
    priority: Priority | None,
    category_id: int | None,
    employee_id: int | None,
    sort_by: SortField,
    sort_order: SortOrder,
    page: int,
    page_size: int,
) -> tuple[list[Complaint], int]:
    statement: Select[tuple[Complaint]] = select(Complaint).options(
        selectinload(Complaint.category),
        selectinload(Complaint.assigned_employee),
        selectinload(Complaint.activities),
    )
    count_statement = select(func.count()).select_from(Complaint)
    filters = []
    if search:
        search_pattern = f"%{search}%"
        filters.append(
            or_(
                Complaint.customer_name.ilike(search_pattern),
                Complaint.customer_contact.ilike(search_pattern),
                Complaint.subject.ilike(search_pattern),
                cast(Complaint.id, String).ilike(search_pattern),
            )
        )
    if status is not None:
        filters.append(Complaint.status == status)
    if priority is not None:
        filters.append(Complaint.priority == priority)
    if category_id is not None:
        filters.append(Complaint.category_id == category_id)
    if employee_id is not None:
        filters.append(Complaint.assigned_employee_id == employee_id)

    statement = statement.where(*filters)
    count_statement = count_statement.where(*filters)
    sort_column = getattr(Complaint, sort_by.value)
    if sort_order == SortOrder.DESC:
        sort_column = sort_column.desc()
    statement = statement.order_by(sort_column, Complaint.id)
    statement = statement.offset((page - 1) * page_size).limit(page_size)
    total = session.scalar(count_statement)
    return list(session.scalars(statement)), total or 0
