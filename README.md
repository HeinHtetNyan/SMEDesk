# SMEDesk

POS + accounting + inventory management for small/medium businesses, built from the `helpSME` requirements and the "Industry" design system. Piloted for Golden Leaf Bakery & Store (Yangon).

## Stack

One frontend codebase, shipped three ways, backed by a Python API with offline-first sync.

| Layer | Choice | Why |
|---|---|---|
| Frontend | Vite + React + TypeScript (SPA) | Static bundle, no server assumptions — the same build wraps into desktop/mobile shells unchanged |
| Desktop | [Tauri](https://tauri.app) | Wraps the frontend into a native Windows app |
| Mobile | [Capacitor](https://capacitorjs.com) | Wraps the frontend into a native Android app |
| Offline sync | [PowerSync](https://www.powersync.com) | Local SQLite on every device, synced to Postgres, with conflict resolution handled for us |
| Backend API | [FastAPI](https://fastapi.tiangolo.com) (Python) | Auth, business logic, receipts — plain JSON API, no templating |
| Database | PostgreSQL | Source of truth; UUID primary keys throughout so offline-created records never collide on sync |
| Auth | JWT + role-based access control | Owner / Manager / Senior Accountant / Junior Accountant, per the requirements doc |
| Tenancy | Multi-tenant SaaS | Every table scoped by `business_id` |

## Structure

```
SMEDesk/
  frontend/    Vite + React + TS app — the shared UI, built once as a static bundle (web/PWA)
  backend/     FastAPI app, SQLAlchemy models, Alembic migrations
  desktop/     Tauri project that wraps frontend/dist into a native Windows app
  mobile/      Capacitor project (+ native android/) that wraps frontend/dist into a native Android app
```

`desktop/` and `mobile/` don't contain app UI code of their own — they build `frontend/` first, then wrap its output. Run `frontend`'s dev server for day-to-day UI work; reach for `desktop`/`mobile` when you need to test the native shell itself.

## Backend — local setup

```bash
cd backend
python -m venv venv
./venv/Scripts/activate          # Windows
pip install -r requirements.txt
cp .env.example .env             # then fill in DATABASE_URL / JWT_SECRET
uvicorn app.main:app --reload
```

Requires a running PostgreSQL instance matching `DATABASE_URL` in `.env`. Once the DB is up:

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

## Frontend — local setup

```bash
cd frontend
npm install
npm run dev
```

## Desktop (Windows, via Tauri) — local setup

```bash
cd desktop
npm install
npm run dev      # builds frontend/, then launches the native window
npm run build    # produces an installer under desktop/src-tauri/target
```

## Mobile (Android, via Capacitor) — local setup

```bash
cd mobile
npm install
npm run sync        # builds frontend/, copies it into the native android/ project
npm run android:open  # opens the project in Android Studio to run/build
```

## Status

Early scaffolding: auth (signup/login/me) and the `Business`/`User` tables are in place. Domain models (customers, suppliers, sales, purchases, production, cash) and the PowerSync sync layer are not built yet — see the requirements doc for the full feature list.
