# Enrollment Verifier System

Full-stack web app for checking grantee names against HEI enrollment lists.

## Stack
- Frontend: React + Vite + Bootstrap 5
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL (SQLite also works for quick local testing)
- Excel processing: pandas + openpyxl
- Fuzzy matching: RapidFuzz

## Main features
- Upload grantee masterlist
- Upload enrollment list
- Exact and fuzzy name matching
- Verification sessions
- Dashboard metrics
- Export results to Excel
- Basic login with seeded admin account
- Audit log storage

## Backend setup
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

Seed admin once:
- POST `/auth/seed-admin`
- default email: `admin@example.com`
- default password: `admin123`

## Frontend setup
```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Open:
- Frontend: http://localhost:5173

## Recommended production deployment
- Frontend on Vercel
- Backend on Render or Railway
- PostgreSQL on Neon or Render Postgres

## Important notes
- This codebase is production-oriented but still a starter implementation.
- For office rollout, add migrations, stronger password policy, refresh tokens, file storage, and more detailed role permissions.
- The backend already supports PostgreSQL through `DATABASE_URL`.
