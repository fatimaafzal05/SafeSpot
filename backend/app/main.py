import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Report
from .schemas import CATEGORIES, ReportCreate, ReportRead, StatusUpdate

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SafeSpot API",
    version="1.0.0",
    description="Privacy-first API for anonymous, non-emergency community safety awareness reports. Never send names, contact details, exact home addresses, or live location.",
)
origins = [origin.strip() for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["*"], allow_headers=["*"])


def require_admin(x_admin_password: str | None = Header(default=None)):
    expected = os.getenv("ADMIN_PASSWORD")
    if not expected:
        raise HTTPException(status_code=503, detail="Admin moderation is not configured.")
    if not x_admin_password or x_admin_password != expected:
        raise HTTPException(status_code=401, detail="Invalid admin password.")


def report_or_404(report_id: int, db: Session) -> Report:
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return report


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.post("/reports", response_model=ReportRead, status_code=status.HTTP_201_CREATED, tags=["reports"])
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    report = Report(**payload.model_dump(), status="pending")
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@app.get("/reports", response_model=list[ReportRead], tags=["reports"])
def list_reports(
    category: str | None = Query(default=None, description="One supported report category"),
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db),
):
    query = select(Report).where(Report.status == "approved")
    if category:
        if category not in CATEGORIES:
            raise HTTPException(422, "Unknown category.")
        query = query.where(Report.category == category)
    if start_date:
        query = query.where(Report.created_at >= start_date)
    if end_date:
        query = query.where(Report.created_at <= end_date)
    if start_date and end_date and start_date > end_date:
        raise HTTPException(422, "Start date must be before end date.")
    return db.scalars(query.order_by(Report.created_at.desc())).all()


@app.get("/reports/{report_id}", response_model=ReportRead, tags=["reports"])
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = report_or_404(report_id, db)
    if report.status != "approved":
        raise HTTPException(404, detail="Report not found.")
    return report


@app.post("/reports/{report_id}/upvote", response_model=ReportRead, tags=["reports"])
def upvote_report(report_id: int, db: Session = Depends(get_db)):
    report = report_or_404(report_id, db)
    if report.status != "approved":
        raise HTTPException(404, detail="Report not found.")
    report.upvote_count += 1
    db.commit()
    db.refresh(report)
    return report


@app.get("/admin/reports", response_model=list[ReportRead], dependencies=[Depends(require_admin)], tags=["moderation"])
def admin_list_reports(report_status: str | None = Query(default=None, alias="status"), db: Session = Depends(get_db)):
    query = select(Report)
    if report_status:
        if report_status not in ("pending", "approved", "rejected", "hidden"):
            raise HTTPException(422, "Unknown report status.")
        query = query.where(Report.status == report_status)
    return db.scalars(query.order_by(Report.created_at.desc())).all()


@app.patch("/admin/reports/{report_id}/status", response_model=ReportRead, dependencies=[Depends(require_admin)], tags=["moderation"])
def update_report_status(report_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    report = report_or_404(report_id, db)
    report.status = payload.status
    db.commit()
    db.refresh(report)
    return report


@app.get("/public/analytics", tags=["analytics"])
def public_analytics(category: str | None = None, days: int = Query(default=30, ge=1, le=365), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    since = now - timedelta(days=days)
    base = select(Report).where(Report.status == "approved", Report.created_at >= since)
    if category:
        if category not in CATEGORIES:
            raise HTTPException(422, "Unknown category.")
        base = base.where(Report.category == category)
    reports = db.scalars(base.order_by(Report.created_at.desc())).all()
    counts = {item: 0 for item in CATEGORIES}
    trend = {}
    for report in reports:
        counts[report.category] += 1
        day = report.created_at.date().isoformat()
        trend[day] = trend.get(day, 0) + 1
    return {"total": len(reports), "reports_this_week": sum(r.created_at >= now - timedelta(days=7) for r in reports), "category_counts": counts, "trend": [{"date": day, "count": count} for day, count in sorted(trend.items())], "recent": reports[:5]}
