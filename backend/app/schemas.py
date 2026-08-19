import re
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator

CATEGORIES = ("Unsafe Street", "Poor Lighting", "Traffic Danger", "Harassment Concern", "Suspicious Activity", "Other")
STATUSES = ("pending", "approved", "rejected", "hidden")
PII_PATTERNS = (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)"))
ADDRESS_PATTERN = re.compile(r"\b\d{1,5}\s+[\w .'-]+\s+(?:street|st\.?|road|rd\.?|avenue|ave\.?|lane|ln\.?|drive|dr\.?|house)\b", re.IGNORECASE)


def reject_pii(value: str) -> str:
    if any(pattern.search(value) for pattern in PII_PATTERNS):
        raise ValueError("Do not include email addresses or phone numbers. Keep reports anonymous.")
    if ADDRESS_PATTERN.search(value):
        raise ValueError("Do not include an exact street or home address. Use a broad landmark or area instead.")
    return value.strip()


class ReportCreate(BaseModel):
    category: Literal["Unsafe Street", "Poor Lighting", "Traffic Danger", "Harassment Concern", "Suspicious Activity", "Other"]
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1500)
    approximate_location_name: str = Field(min_length=2, max_length=120)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    incident_at: datetime | None = None

    @field_validator("title", "description", "approximate_location_name")
    @classmethod
    def no_contact_details(cls, value: str) -> str:
        return reject_pii(value)

    @field_validator("latitude", "longitude")
    @classmethod
    def coarse_coordinates(cls, value: float | None) -> float | None:
        # Three decimal places is roughly block-level precision, not a live or exact private location.
        return round(value, 3) if value is not None else None

    @model_validator(mode="after")
    def coordinates_together(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("Provide both latitude and longitude, or leave both blank.")
        return self


class ReportRead(BaseModel):
    id: int
    category: str
    title: str
    description: str
    latitude: float | None
    longitude: float | None
    approximate_location_name: str
    incident_at: datetime | None
    created_at: datetime
    status: str
    upvote_count: int

    model_config = {"from_attributes": True}


class StatusUpdate(BaseModel):
    status: Literal["pending", "approved", "rejected", "hidden"]
