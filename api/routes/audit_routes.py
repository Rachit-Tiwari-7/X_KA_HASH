from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/audit", tags=["audit"])

_audit_logs: list[dict[str, Any]] = []


@router.get("/logs")
async def audit_logs(limit: int = 100):
    return {"logs": _audit_logs[-limit:]}


@router.post("/log")
async def create_log(entry: dict):
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    _audit_logs.append(entry)
    logger.info("Audit log: %s", entry.get("action", "unknown"))
    return {"status": "ok"}
