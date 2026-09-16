"""create complaint management tables

Revision ID: 20260916_1200
Revises:
Create Date: 2026-09-16 12:00:00

"""
from collections.abc import Sequence

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


revision: str = "20260916_1200"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


priority_enum = postgresql.ENUM(
    "LOW", "MEDIUM", "HIGH", "CRITICAL", name="priority", create_type=False
)
status_enum = postgresql.ENUM(
    "NEW",
    "ASSIGNED",
    "IN_PROGRESS",
    "RESOLVED",
    "CLOSED",
    name="status",
    create_type=False,
)
utc_now = sa.text("TIMEZONE('utc', now())")


def upgrade() -> None:
    # Use PostgreSQL's duplicate_object exception so this remains safe after a
    # previous attempt created one or both types before failing.
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE priority AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
        EXCEPTION
            WHEN duplicate_object THEN NULL;
        END
        $$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            CREATE TYPE status AS ENUM (
                'NEW', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'
            );
        EXCEPTION
            WHEN duplicate_object THEN NULL;
        END
        $$;
        """
    )

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("department", sa.String(length=150), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=utc_now, nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=utc_now, nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "complaints",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_name", sa.String(length=150), nullable=False),
        sa.Column("customer_contact", sa.String(length=320), nullable=False),
        sa.Column("subject", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("priority", priority_enum, nullable=False),
        sa.Column("assigned_employee_id", sa.Integer(), nullable=True),
        sa.Column("expected_resolution_date", sa.Date(), nullable=False),
        sa.Column("status", status_enum, server_default=sa.text("'NEW'"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=utc_now, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=utc_now, nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["assigned_employee_id"], ["employees.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="RESTRICT"),
    )
    op.create_table(
        "complaint_activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("performed_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=utc_now, nullable=False),
        sa.ForeignKeyConstraint(["complaint_id"], ["complaints.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["performed_by"], ["employees.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("complaint_activities")
    op.drop_table("complaints")
    op.drop_table("categories")
    op.drop_table("employees")
    status_enum.drop(op.get_bind(), checkfirst=True)
    priority_enum.drop(op.get_bind(), checkfirst=True)
