"""
Vertex Platform — Checkout Service
Orchestrates an order: checks inventory, then triggers notification.
This is where a slow downstream dependency (notification-service)
shows up as elevated latency and, eventually, timeouts.
"""

import os
import random
import time
import uuid

import httpx
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI(title="Vertex Checkout Service", version="1.0.0")
Instrumentator().instrument(app).expose(app)

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8002")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "http://notification-service:8003")
DOWNSTREAM_TIMEOUT = float(os.getenv("DOWNSTREAM_TIMEOUT", "5.0"))

_orders = {}


class CheckoutRequest(BaseModel):
    sku: str
    quantity: int = 1
    customer_email: str = "demo@example.com"


@app.get("/health")
async def health():
    return {"status": "ok", "service": "checkout-service"}


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = _orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/checkout")
async def checkout(req: CheckoutRequest):
    order_id = str(uuid.uuid4())[:8]
    start = time.time()

    async with httpx.AsyncClient(timeout=DOWNSTREAM_TIMEOUT) as client:
        # 1. Check inventory.
        try:
            inv_resp = await client.post(
                f"{INVENTORY_URL}/stock/check",
                json={"sku": req.sku, "quantity": req.quantity},
            )
            inv_resp.raise_for_status()
            stock_ok = inv_resp.json().get("available", False)
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Inventory service unavailable")

        if not stock_ok:
            raise HTTPException(status_code=409, detail="Insufficient stock")

        # 2. Trigger notification (the dependency we can slow down live).
        notify_status = "skipped"
        try:
            notify_resp = await client.post(
                f"{NOTIFICATION_URL}/notify",
                json={"order_id": order_id, "channel": "email"},
            )
            notify_status = "sent" if notify_resp.status_code == 200 else "failed"
        except httpx.TimeoutException:
            notify_status = "timeout"
        except httpx.HTTPError:
            notify_status = "failed"

    order = {
        "order_id": order_id,
        "sku": req.sku,
        "quantity": req.quantity,
        "customer_email": req.customer_email,
        "notification_status": notify_status,
        "duration_ms": round((time.time() - start) * 1000, 1),
    }
    _orders[order_id] = order
    return order
