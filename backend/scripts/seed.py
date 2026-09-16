"""Seed a fresh complaint management database with representative data."""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Category, Complaint, ComplaintActivity, Employee, Priority, Status


EMPLOYEES = [
    {
        "name": "Maya Patel",
        "email": "maya.patel@example.com",
        "department": "Customer Support",
    },
    {
        "name": "Liam Chen",
        "email": "liam.chen@example.com",
        "department": "Technical Support",
    },
    {
        "name": "Sofia Martinez",
        "email": "sofia.martinez@example.com",
        "department": "Billing Operations",
    },
    {
        "name": "Noah Williams",
        "email": "noah.williams@example.com",
        "department": "Delivery Operations",
    },
    {
        "name": "Aisha Khan",
        "email": "aisha.khan@example.com",
        "department": "Customer Success",
    },
]

CATEGORY_NAMES = ["Billing", "Technical", "Delivery", "Product", "Service", "Other"]


def complaint_definitions(today: date) -> list[dict]:
    return [
        {
            "customer_name": "Evelyn Brooks",
            "customer_contact": "evelyn.brooks@example.com",
            "subject": "Duplicate charge on September invoice",
            "description": "The customer was charged twice for the same annual subscription renewal.",
            "category": "Billing",
            "priority": Priority.HIGH,
            "employee": "sofia.martinez@example.com",
            "due": today - timedelta(days=4),
            "status": Status.IN_PROGRESS,
            "activities": [
                ("Submitted", "Customer reported two identical charges on the invoice."),
                ("Assigned", "Assigned to Billing Operations for payment review."),
                ("Investigating", "Payment ledger and invoice history are being compared."),
            ],
        },
        {
            "customer_name": "Marcus Reed",
            "customer_contact": "marcus.reed@example.com",
            "subject": "Unable to reset account password",
            "description": "Password reset emails are not arriving despite several attempts.",
            "category": "Technical",
            "priority": Priority.HIGH,
            "employee": "liam.chen@example.com",
            "due": today - timedelta(days=2),
            "status": Status.ASSIGNED,
            "activities": [
                ("Submitted", "Customer reported repeated password reset failures."),
                ("Assigned", "Assigned to Technical Support for account email diagnostics."),
            ],
        },
        {
            "customer_name": "Olivia Turner",
            "customer_contact": "olivia.turner@example.com",
            "subject": "Package has not arrived",
            "description": "The order was marked as dispatched six days ago but has not arrived.",
            "category": "Delivery",
            "priority": Priority.HIGH,
            "employee": "noah.williams@example.com",
            "due": today - timedelta(days=1),
            "status": Status.IN_PROGRESS,
            "activities": [
                ("Submitted", "Customer requested an update for a delayed package."),
                ("Assigned", "Assigned to Delivery Operations to contact the carrier."),
                ("Carrier Check", "Carrier trace opened for the missing shipment."),
            ],
        },
        {
            "customer_name": "Daniel Foster",
            "customer_contact": "daniel.foster@example.com",
            "subject": "Refund not received after return",
            "description": "The customer returned the product two weeks ago and is still waiting for the refund.",
            "category": "Billing",
            "priority": Priority.CRITICAL,
            "employee": "sofia.martinez@example.com",
            "due": today + timedelta(days=1),
            "status": Status.IN_PROGRESS,
            "activities": [
                ("Submitted", "Customer followed up about a missing return refund."),
                ("Assigned", "Assigned to Billing Operations for refund reconciliation."),
                ("Escalated", "Refund exception escalated for manual payment processing."),
            ],
        },
        {
            "customer_name": "Grace Kim",
            "customer_contact": "grace.kim@example.com",
            "subject": "Mobile app crashes at checkout",
            "description": "The Android app closes whenever the customer taps the final checkout button.",
            "category": "Technical",
            "priority": Priority.CRITICAL,
            "employee": "liam.chen@example.com",
            "due": today + timedelta(days=2),
            "status": Status.ASSIGNED,
            "activities": [
                ("Submitted", "Customer supplied device details and a checkout screen recording."),
                ("Assigned", "Assigned to Technical Support for reproduction."),
            ],
        },
        {
            "customer_name": "Henry Wallace",
            "customer_contact": "henry.wallace@example.com",
            "subject": "Incorrect color received",
            "description": "The delivered item is the wrong color compared with the confirmed order.",
            "category": "Product",
            "priority": Priority.MEDIUM,
            "employee": "maya.patel@example.com",
            "due": today + timedelta(days=3),
            "status": Status.NEW,
            "activities": [
                ("Submitted", "Customer provided photos of the received item and order confirmation."),
            ],
        },
        {
            "customer_name": "Chloe Bennett",
            "customer_contact": "chloe.bennett@example.com",
            "subject": "Request to update delivery address",
            "description": "The customer moved and needs an address correction before dispatch.",
            "category": "Delivery",
            "priority": Priority.LOW,
            "employee": None,
            "due": today + timedelta(days=5),
            "status": Status.NEW,
            "activities": [
                ("Submitted", "Customer requested an address change before fulfillment."),
            ],
        },
        {
            "customer_name": "Samuel Ortiz",
            "customer_contact": "samuel.ortiz@example.com",
            "subject": "Subscription feature missing",
            "description": "A feature listed in the customer subscription is not available in the account.",
            "category": "Product",
            "priority": Priority.MEDIUM,
            "employee": "aisha.khan@example.com",
            "due": today + timedelta(days=4),
            "status": Status.IN_PROGRESS,
            "activities": [
                ("Submitted", "Customer identified a missing feature from the subscription plan."),
                ("Assigned", "Assigned to Customer Success for plan verification."),
                ("Investigating", "Subscription entitlement is being checked against the product catalog."),
            ],
        },
        {
            "customer_name": "Isabella Moore",
            "customer_contact": "isabella.moore@example.com",
            "subject": "Support callback was missed",
            "description": "The customer waited for a scheduled callback that did not take place.",
            "category": "Service",
            "priority": Priority.HIGH,
            "employee": "maya.patel@example.com",
            "due": today - timedelta(days=3),
            "status": Status.RESOLVED,
            "resolved_days_ago": 1,
            "activities": [
                ("Submitted", "Customer reported a missed callback appointment."),
                ("Assigned", "Assigned to Customer Support for callback review."),
                ("Resolved", "Callback completed and a new appointment process was arranged."),
            ],
        },
        {
            "customer_name": "James Carter",
            "customer_contact": "james.carter@example.com",
            "subject": "Order marked delivered but missing",
            "description": "Tracking shows delivery completed, but the customer cannot locate the parcel.",
            "category": "Delivery",
            "priority": Priority.HIGH,
            "employee": "noah.williams@example.com",
            "due": today - timedelta(days=5),
            "status": Status.RESOLVED,
            "resolved_days_ago": 2,
            "activities": [
                ("Submitted", "Customer reported a delivery scan without receiving the parcel."),
                ("Assigned", "Assigned to Delivery Operations for proof-of-delivery review."),
                ("Resolved", "Carrier confirmed a neighbor delivery and the parcel was recovered."),
            ],
        },
        {
            "customer_name": "Amelia Scott",
            "customer_contact": "amelia.scott@example.com",
            "subject": "Invoice company name correction",
            "description": "The customer needs the legal company name corrected on a recent invoice.",
            "category": "Billing",
            "priority": Priority.LOW,
            "employee": "sofia.martinez@example.com",
            "due": today - timedelta(days=7),
            "status": Status.CLOSED,
            "resolved_days_ago": 5,
            "closed_days_ago": 3,
            "activities": [
                ("Submitted", "Customer requested a correction to invoice account details."),
                ("Assigned", "Assigned to Billing Operations."),
                ("Resolved", "Invoice was regenerated with the corrected legal company name."),
                ("Closed", "Customer confirmed the updated invoice was received."),
            ],
        },
        {
            "customer_name": "Ethan Hughes",
            "customer_contact": "ethan.hughes@example.com",
            "subject": "Product arrived damaged",
            "description": "The customer received a damaged device and requested a replacement.",
            "category": "Product",
            "priority": Priority.CRITICAL,
            "employee": "aisha.khan@example.com",
            "due": today - timedelta(days=6),
            "status": Status.CLOSED,
            "resolved_days_ago": 4,
            "closed_days_ago": 2,
            "activities": [
                ("Submitted", "Customer uploaded photographs showing transit damage."),
                ("Assigned", "Assigned to Customer Success for replacement coordination."),
                ("Resolved", "Replacement device shipped with expedited delivery."),
                ("Closed", "Customer confirmed the replacement arrived in good condition."),
            ],
        },
        {
            "customer_name": "Mia Richardson",
            "customer_contact": "mia.richardson@example.com",
            "subject": "Need help understanding account settings",
            "description": "The customer is unsure how to configure notification preferences.",
            "category": "Service",
            "priority": Priority.LOW,
            "employee": None,
            "due": today + timedelta(days=6),
            "status": Status.NEW,
            "activities": [
                ("Submitted", "Customer asked for guidance on notification preferences."),
            ],
        },
        {
            "customer_name": "Lucas Evans",
            "customer_contact": "lucas.evans@example.com",
            "subject": "Unexpected service fee",
            "description": "A service fee appeared on the latest statement without an obvious explanation.",
            "category": "Other",
            "priority": Priority.MEDIUM,
            "employee": "maya.patel@example.com",
            "due": today + timedelta(days=2),
            "status": Status.ASSIGNED,
            "activities": [
                ("Submitted", "Customer questioned an unfamiliar service fee."),
                ("Assigned", "Assigned to Customer Support for account review."),
            ],
        },
        {
            "customer_name": "Nora Adams",
            "customer_contact": "nora.adams@example.com",
            "subject": "Unable to download purchase receipt",
            "description": "The receipt download link returns an error from the order history page.",
            "category": "Technical",
            "priority": Priority.MEDIUM,
            "employee": "liam.chen@example.com",
            "due": today + timedelta(days=7),
            "status": Status.IN_PROGRESS,
            "activities": [
                ("Submitted", "Customer reported an error while downloading a receipt."),
                ("Assigned", "Assigned to Technical Support."),
                ("Investigating", "Receipt generation logs are being reviewed for the affected order."),
            ],
        },
        {
            "customer_name": "Benjamin Price",
            "customer_contact": "benjamin.price@example.com",
            "subject": "Product instructions are unclear",
            "description": "The included setup instructions do not explain the required first-time configuration.",
            "category": "Product",
            "priority": Priority.LOW,
            "employee": None,
            "due": today + timedelta(days=8),
            "status": Status.NEW,
            "activities": [
                ("Submitted", "Customer requested clearer setup instructions."),
            ],
        },
        {
            "customer_name": "Harper Wilson",
            "customer_contact": "harper.wilson@example.com",
            "subject": "Delivery window changed without notice",
            "description": "The scheduled delivery window changed on the morning of delivery.",
            "category": "Delivery",
            "priority": Priority.MEDIUM,
            "employee": "noah.williams@example.com",
            "due": today + timedelta(days=1),
            "status": Status.ASSIGNED,
            "activities": [
                ("Submitted", "Customer reported an unexpected delivery window change."),
                ("Assigned", "Assigned to Delivery Operations to review carrier notifications."),
            ],
        },
        {
            "customer_name": "William Grant",
            "customer_contact": "william.grant@example.com",
            "subject": "Service response took too long",
            "description": "The customer waited five business days for an answer to a product question.",
            "category": "Service",
            "priority": Priority.HIGH,
            "employee": "aisha.khan@example.com",
            "due": today - timedelta(days=2),
            "status": Status.RESOLVED,
            "resolved_days_ago": 1,
            "activities": [
                ("Submitted", "Customer raised a concern about delayed support response."),
                ("Assigned", "Assigned to Customer Success for service review."),
                ("Resolved", "Response-time concern addressed and the requested product guidance provided."),
            ],
        },
    ]


def utc_at(day: date) -> datetime:
    return datetime.combine(day, time.min, tzinfo=timezone.utc)


def get_or_create_employees(session) -> dict[str, Employee]:
    employees = {}
    for definition in EMPLOYEES:
        employee = session.scalar(
            select(Employee).where(Employee.email == definition["email"])
        )
        if employee is None:
            employee = Employee(**definition)
            session.add(employee)
            session.flush()
        employees[definition["email"]] = employee
    return employees


def get_or_create_categories(session) -> dict[str, Category]:
    categories = {}
    for name in CATEGORY_NAMES:
        category = session.scalar(select(Category).where(Category.name == name))
        if category is None:
            category = Category(name=name)
            session.add(category)
            session.flush()
        categories[name] = category
    return categories


def seed_complaints(session, employees, categories, today: date) -> int:
    created_count = 0
    for definition in complaint_definitions(today):
        complaint = session.scalar(
            select(Complaint).where(
                Complaint.customer_contact == definition["customer_contact"],
                Complaint.subject == definition["subject"],
            )
        )
        if complaint is None:
            employee = (
                employees[definition["employee"]]
                if definition["employee"] is not None
                else None
            )
            resolved_at = (
                utc_at(today - timedelta(days=definition["resolved_days_ago"]))
                if "resolved_days_ago" in definition
                else None
            )
            closed_at = (
                utc_at(today - timedelta(days=definition["closed_days_ago"]))
                if "closed_days_ago" in definition
                else None
            )
            complaint = Complaint(
                customer_name=definition["customer_name"],
                customer_contact=definition["customer_contact"],
                subject=definition["subject"],
                description=definition["description"],
                category=categories[definition["category"]],
                priority=definition["priority"],
                assigned_employee=employee,
                expected_resolution_date=definition["due"],
                status=definition["status"],
                resolved_at=resolved_at,
                closed_at=closed_at,
            )
            session.add(complaint)
            session.flush()
            for action, description in definition["activities"]:
                performed_by = (
                    employee.id
                    if employee is not None
                    else None
                )
                session.add(
                    ComplaintActivity(
                        complaint_id=complaint.id,
                        action=action,
                        description=description,
                        performed_by=performed_by,
                    )
                )
            created_count += 1
    return created_count


def main() -> None:
    today = datetime.now(timezone.utc).date()
    with SessionLocal.begin() as session:
        employees = get_or_create_employees(session)
        categories = get_or_create_categories(session)
        created_count = seed_complaints(session, employees, categories, today)
    print(f"Seed complete: {created_count} new complaints created.")


if __name__ == "__main__":
    main()
