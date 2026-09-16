from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category, Employee
from ..schemas.directory import CategoryResponse, EmployeeResponse

router = APIRouter(tags=["directory"])


@router.get("/employees", response_model=list[EmployeeResponse])
def read_employees(session: Session = Depends(get_db)) -> list[Employee]:
    return list(session.scalars(select(Employee).order_by(Employee.name)))


@router.get("/categories", response_model=list[CategoryResponse])
def read_categories(session: Session = Depends(get_db)) -> list[Category]:
    return list(session.scalars(select(Category).order_by(Category.name)))
