# SafeSpot

SafeSpot is a portfolio-ready community safety awareness platform for **anonymous, non-emergency** reports such as unsafe streets, poor lighting, traffic danger, harassment concerns, and suspicious activity. It deliberately avoids accounts, paid APIs, tracking, real-time location, and personal data collection.

> **Emergency notice:** SafeSpot is for non-emergency community awareness. If there is immediate danger, contact local emergency services.

## Why SafeSpot is useful

Communities often notice recurring safety issues—an unlit crossing, a hazardous road edge, or a pattern of concerning activity—before there is a clear public record of them. SafeSpot provides a responsible middle ground: people can surface broad, useful local context without creating an emergency dispatch tool or exposing someone’s identity.

Reports are anonymous, reviewed before publication, and displayed only at a coarse community level. This helps residents recognize patterns and make informed day-to-day decisions while respecting privacy, avoiding blame, and keeping urgent incidents with the appropriate emergency services.

### Design principles

- **Privacy first:** no accounts, names, contact details, exact addresses, precise coordinates, or live tracking.
- **Moderation before reach:** every new report starts as `pending`; only approved reports appear publicly.
- **Useful, not alarming:** the map and dashboard communicate longer-term community context—not real-time alerts or crime claims.
- **Accessible by default:** responsive layouts, visible labels, keyboard-friendly controls, clear loading and empty states.

## Features

- Privacy-aware anonymous reporting with server-side checks for email addresses and phone numbers.
- FastAPI + SQLite API with automatic interactive documentation.
- Approval workflow: pending reports are invisible to public pages until approved.
- Responsive Next.js dashboard, category/time filters, lightweight charts, accessibility labels, loading/error/empty states.
- Leaflet + OpenStreetMap community map using only voluntarily supplied broad coordinates. Reports without coordinates appear below the map instead.
- Password-protected portfolio moderation panel; the password stays on the server.

## Technology choices

| Layer | Technology | Why |
| --- | --- | --- |
| Web app | Next.js, React, CSS Modules | Fast, responsive interface with maintainable component-scoped styles. |
| API | FastAPI, Pydantic | Typed request validation and clear automatic OpenAPI documentation. |
| Data | SQLite, SQLAlchemy | Lightweight local development with an explicit, portable data model. |
| Map | Leaflet, OpenStreetMap | Open-source mapping with no paid map API dependency. |

## Project structure

```
SafeSpot/
├── backend/                 # FastAPI, SQLAlchemy, SQLite
│   ├── app/main.py          # API routes and API documentation metadata
│   ├── app/models.py        # Report database model
│   └── .env.example
├── frontend/                # Next.js App Router + CSS Modules
│   ├── app/                 # Dashboard, report, map, tips, admin pages
│   ├── components/
│   └── .env.example
└── README.md
```

## Run locally

Prerequisites: Python 3.10+ and Node.js 20+.

1. In one terminal, start the API:

   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   Copy-Item .env.example .env
   # Edit .env and set ADMIN_PASSWORD to your own long local password.
   uvicorn app.main:app --reload
   ```

   The API runs at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive OpenAPI documentation.

2. In another terminal, start the web app:

   ```powershell
   cd frontend
   Copy-Item .env.example .env.local
   npm install
   npm run dev
   ```

   Open `http://localhost:3000`.

The SQLite database is created automatically as `backend/safespot.db`. It is ignored by Git. To reset sample/local data during development, stop the API and delete only that file.

## API routes

Public routes expose approved reports only:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/reports` | Submit an anonymous report (initially `pending`) |
| `GET` | `/reports?category=&start_date=&end_date=` | List approved reports and filter by category/date |
| `GET` | `/reports/{id}` | Get an approved report |
| `POST` | `/reports/{id}/upvote` | Add community support to an approved report |
| `GET` | `/public/analytics?category=&days=` | Dashboard metrics and chart data |
| `GET` | `/admin/reports?status=pending` | Admin-only moderation queue |
| `PATCH` | `/admin/reports/{id}/status` | Approve, reject, hide, or restore a report |

Admin requests require the `X-Admin-Password` header. OpenAPI docs are available at `/docs` and the raw schema at `/openapi.json`.

## Privacy and moderation

Do not enter names, phone numbers, email addresses, exact home addresses, photos, or live location. The form asks for a broad landmark/area and makes coordinates optional; coordinates accepted by the API are rounded to three decimal places. Moderation should reject anything that might identify a person or reveal a sensitive private location. This portfolio build applies basic automated checks, but human moderation remains essential.

Set `ADMIN_PASSWORD` in `backend/.env`; never place it in `frontend/.env.local` or source code. For a real product, replace this demonstration password flow with proper server-side authentication and rate limiting.

## Deployment guide

### Frontend: Vercel

1. Push this repository to GitHub and import it in Vercel.
2. Set the project root directory to `frontend`.
3. Add `NEXT_PUBLIC_API_URL` with the deployed HTTPS backend URL.
4. Deploy with the detected Next.js settings.

### Backend: a free Python host

Use a provider offering a free Python web-service tier, such as Render’s free tier when available, or deploy to another provider that supports FastAPI. Set its root directory to `backend`, use build command `pip install -r requirements.txt`, and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Add `ADMIN_PASSWORD` and set `FRONTEND_ORIGINS` to your Vercel domain. SQLite is suitable for a local demo; use provider-backed persistent storage or a managed database before relying on deployments, since many free hosts have ephemeral disks.

## Screenshots

Add portfolio screenshots here after running the app:

- `[Dashboard screenshot — add image]`
- `[Community map screenshot — add image]`
- `[Report form screenshot — add image]`
- `[Moderation queue screenshot — add image]`

## Portfolio/CV description

Built **SafeSpot**, a privacy-first full-stack community safety awareness platform using Next.js, React, CSS Modules, FastAPI, SQLAlchemy, SQLite, Leaflet, and OpenStreetMap. Designed anonymous reporting and human moderation workflows, responsive data visualizations, and public-map privacy controls without paid services or personal-data tracking.
