# Customer Complaint Management System

A full-stack complaint operations workspace for recording customer issues, tracking ownership, managing priorities, and moving complaints through a controlled resolution workflow.

## Key features

- Dashboard with live totals, status and priority distributions, recent complaints, and overdue counts.
- Complaint search, filtering, sorting, pagination, creation, editing, and detail views.
- Employee assignment and validated workflow transitions with activity history.
- Overdue complaint indicators and resolution/closure timestamps.
- Idempotent seed data for employees, categories, complaints, and activities.
- PostgreSQL migrations managed with Alembic.

## Tech stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python
- **Data layer:** SQLAlchemy, Alembic
- **Database:** Supabase PostgreSQL

## Architecture

```text
Next.js → FastAPI → SQLAlchemy → Supabase PostgreSQL
```

The frontend calls the FastAPI REST API. The backend owns validation, complaint business rules, workflow transitions, activity creation, and database access.

## Project structure

```text
/
├── frontend/              # Next.js application
│   ├── app/               # Dashboard, complaint list, create, and detail pages
│   ├── components/        # Shared layout and UI components
│   └── lib/api.ts         # Typed API client
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── models/        # SQLAlchemy models and enums
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── routers/       # Thin API route handlers
│   │   └── services/      # Complaint and dashboard business logic
│   ├── migrations/        # Alembic migration scripts
│   └── scripts/seed.py    # Repeatable seed script
└── README.md
```

## Local setup

### Prerequisites

- Node.js 18.17+
- Python 3.11+
- A Supabase PostgreSQL database

### Backend

From the repository root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set the backend variables described below, then run migrations and optional seed data:

```powershell
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:3000`.

## Environment variables

Create `backend/.env`:

```env
DATABASE_URL=postgresql://<user>:<password>@<supabase-host>:5432/postgres
FRONTEND_URL=http://localhost:3000
```

Create or update `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

The backend normalizes standard PostgreSQL connection URLs for the Psycopg SQLAlchemy driver. Use the Supabase connection string appropriate for your environment.

`DATABASE_URL` and `NEXT_PUBLIC_API_URL` are required for a local installation. `FRONTEND_URL` can be set when the frontend runs on a different origin; localhost and `127.0.0.1` development origins are already supported.

**Never commit real credentials, database URLs, API keys, or other secrets.** Keep local `.env` files out of version control and share only redacted examples.

## API overview

Base URL: `http://localhost:8000`

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | API health check |
| GET | `/dashboard/summary` | Dashboard totals and status/priority counts |
| GET | `/employees` | Employee dropdown data |
| GET | `/categories` | Category dropdown data |
| GET | `/complaints` | Search, filter, sort, and paginate complaints |
| GET | `/complaints/{id}` | Retrieve complaint details and activity history |
| POST | `/complaints` | Create a new complaint |
| PATCH | `/complaints/{id}` | Edit allowed complaint fields |
| POST | `/complaints/{id}/assign` | Assign a NEW complaint |
| POST | `/complaints/{id}/transition` | Move a complaint to its next workflow status |

Interactive API documentation is available at `/docs` when the backend is running.

## Complaint workflow

```text
NEW → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED
```

New complaints always start as `NEW` and unassigned. Assignment is only allowed from `NEW`; workflow transitions are validated by the backend. Resolving sets `resolved_at`, closing sets `closed_at`, and every assignment or transition creates a complaint activity record.

## Database migrations and seed data

Alembic manages schema migrations:

```powershell
cd backend
alembic upgrade head
```

The seed script creates representative data and is safe to run repeatedly:

```powershell
python -m scripts.seed
```

## Development note

The project was developed with AI-assisted development alongside manual engineering review, testing, and verification. Application behavior, API contracts, database rules, and production configuration remain explicitly defined by the project implementation.
