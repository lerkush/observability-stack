"""
Vertex Platform — Notification Service
Sends order confirmation emails/SMS. In real life, this depends on a
third-party provider (SendGrid, Twilio, etc.) — which is exactly why
it's the most common source of cascading latency in production.

This service exposes an admin endpoint to inject artificial latency,
used to demonstrate the alerting pipeline live.
"""

import asyncio
import random
import time

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI(title="Vertex Notification Service", version="1.0.0")
Instrumentator().instrument(app).expose(app)

# Shared in-memory "incident" toggle — when active, requests are slowed down
# to simulate a degraded third-party provider.
_state = {
    "injected_latency_seconds": 0.0,
    "injected_until": 0.0,
}


class NotifyRequest(BaseModel):
    order_id: str
    channel: str = "email"


class LatencyInjectRequest(BaseModel):
    seconds: float = 3.0
    duration_seconds: float = 120.0


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification-service"}


@app.post("/notify")
async def notify(req: NotifyRequest):
    # Simulate the current injected incident, if any.
    if time.time() < _state["injected_until"]:
        await asyncio.sleep(_state["injected_latency_seconds"])

    # Normal jitter, as any real network call to a third party would have.
    await asyncio.sleep(random.uniform(0.02, 0.12))

    # Small, realistic baseline failure rate (provider hiccups).
    if random.random() < 0.02:
        raise HTTPException(status_code=502, detail="Upstream provider error")

    return {"order_id": req.order_id, "channel": req.channel, "status": "sent"}


@app.post("/admin/inject-latency")
async def inject_latency(req: LatencyInjectRequest):
    """Used live in demos: simulates the notification provider degrading."""
    _state["injected_latency_seconds"] = req.seconds
    _state["injected_until"] = time.time() + req.duration_seconds
    return {
        "message": f"Injecting {req.seconds}s latency for {req.duration_seconds}s",
        "active_until_epoch": _state["injected_until"],
    }


@app.post("/admin/clear-incident")
async def clear_incident():
    _state["injected_latency_seconds"] = 0.0
    _state["injected_until"] = 0.0
    return {"message": "Incident cleared"}
