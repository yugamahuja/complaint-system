# Customer Complaint Management System

Initial monorepo foundation for a customer complaint management system.

## Prerequisites

- Node.js 18.17+
- Python 3.11+
- PostgreSQL (for future database-backed features)

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --env-file .env
```

The API is available at http://localhost:8000 and its health endpoint is
http://localhost:8000/health.

Set `DATABASE_URL` in `backend/.env` to the PostgreSQL connection string for
your local database.

## Database migrations

After PostgreSQL is running and `DATABASE_URL` is configured:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
alembic upgrade head
```

To load representative employees, categories, complaints, and activity history:

```powershell
python -m scripts.seed
```

The seed command is safe to run repeatedly; existing seed records are reused.
