from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.complaint import Priority, Status
from ..schemas.complaint import (
    ComplaintCreate,
    ComplaintAssignment,
    ComplaintListResponse,
    ComplaintResponse,
    ComplaintTransition,
    ComplaintUpdate,
    PriorityFilter,
    SortField,
    SortOrder,
    StatusFilter,
)
from ..services.complaints import (
    ComplaintNotFoundError,
    ComplaintValidationError,
    ComplaintWorkflowError,
    assign_complaint,
    create_complaint,
    get_complaint,
    list_complaints,
    update_complaint,
    transition_complaint,
)

router = APIRouter(prefix="/complaints", tags=["complaints"])


def _not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Complaint not found")


@router.get("", response_model=ComplaintListResponse)
def read_complaints(
    search: str | None = Query(default=None, min_length=1),
    status_filter: StatusFilter | None = Query(default=None, alias="status"),
    priority_filter: PriorityFilter | None = Query(default=None, alias="priority"),
    category_id: int | None = Query(default=None, gt=0),
    employee_id: int | None = Query(default=None, gt=0),
    sort_by: SortField = SortField.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_db),
) -> ComplaintListResponse:
    items, total = list_complaints(
        session,
        search=search,
        status=Status(status_filter.value) if status_filter else None,
        priority=Priority(priority_filter.value) if priority_filter else None,
        category_id=category_id,
        employee_id=employee_id,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return ComplaintListResponse(items=items, page=page, page_size=page_size, total=total)


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def read_complaint(complaint_id: int, session: Session = Depends(get_db)) -> ComplaintResponse:
    try:
        return get_complaint(session, complaint_id)
    except ComplaintNotFoundError:
        raise _not_found()


@router.post("/{complaint_id}/assign", response_model=ComplaintResponse)
def assign_existing_complaint(
    complaint_id: int,
    data: ComplaintAssignment,
    session: Session = Depends(get_db),
) -> ComplaintResponse:
    try:
        return assign_complaint(session, complaint_id, data.employee_id, data.description)
    except ComplaintNotFoundError:
        raise _not_found()
    except ComplaintValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except ComplaintWorkflowError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.post("/{complaint_id}/transition", response_model=ComplaintResponse)
def transition_existing_complaint(
    complaint_id: int,
    data: ComplaintTransition,
    session: Session = Depends(get_db),
) -> ComplaintResponse:
    try:
        return transition_complaint(
            session, complaint_id, data.status, data.description
        )
    except ComplaintNotFoundError:
        raise _not_found()
    except ComplaintWorkflowError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.post(
    "",
    response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_complaint(
    data: ComplaintCreate, session: Session = Depends(get_db)
) -> ComplaintResponse:
    try:
        return create_complaint(session, data)
    except ComplaintValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def patch_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    session: Session = Depends(get_db),
) -> ComplaintResponse:
    try:
        return update_complaint(session, complaint_id, data)
    except ComplaintNotFoundError:
        raise _not_found()
    except ComplaintValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
