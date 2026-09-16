from typing import TYPE_CHECKING, List

from datetime import datetime

from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .complaint import Complaint, ComplaintActivity


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("TIMEZONE('utc', now())"),
    )

    assigned_complaints: Mapped[List["Complaint"]] = relationship(
        back_populates="assigned_employee", foreign_keys="Complaint.assigned_employee_id"
    )
    complaint_activities: Mapped[List["ComplaintActivity"]] = relationship(
        back_populates="performer", foreign_keys="ComplaintActivity.performed_by"
    )
