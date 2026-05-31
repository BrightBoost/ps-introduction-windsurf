from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    rejected = "rejected"


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    status: ApplicationStatus
    applied_date: date
    notes: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    notes: Optional[str] = None


class JobApplication(BaseModel):
    id: int
    company: str
    role: str
    status: ApplicationStatus
    applied_date: date
    notes: Optional[str] = None


class ApplicationSummary(BaseModel):
    total: int
    by_status: dict[str, int]
    response_rate: float
    success_rate: float
    rejection_rate: float
    most_recent: JobApplication | None
