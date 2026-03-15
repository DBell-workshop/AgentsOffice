from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


TaskStatus = Literal["pending", "running", "succeeded", "failed"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


class TaskRecord(BaseModel):
    task_id: str
    trace_id: str
    task_type: str
    status: TaskStatus = "pending"
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)
    input: dict[str, Any] = Field(default_factory=dict)
    output: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class ApiEnvelope(BaseModel):
    trace_id: str
    request_id: str
    data: dict[str, Any]
    error: Optional[str] = None
