"""
Vertex Platform — Gateway Service
Public entry point. Forwards checkout requests to checkout-service.
Also exposes a /demo/traffic endpoint that generates a burst of
realistic synthetic traffic, useful for live demos.
"""

import asyncio
import os
import random

import httpx
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI(title="Vertex Gateway Service", version="1.0.0")
Instrumentator().instrument(app).expose(app)

CHECKOUT_URL = os.getenv("CHECKOUT_URL", "http://checkout-service:8001")
SAMPLE_SKUS = [f"sku-{i}" for i in range(1, 21)]


class CheckoutPassthrough(BaseModel):
    sku: str
    quantity: int = 1
    customer_email: str = "demo@example.com"


@app.get("/health")
async def health():
    return {"status": "ok", "service": "gateway-service"}


@app.post("/checkout")
async def checkout(req: CheckoutPassthrough):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(f"{CHECKOUT_URL}/checkout", json=req.dict())
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Checkout service unavailable")
    return resp.json() if resp.status_code < 400 else HTTPException(
        status_code=resp.status_code, detail=resp.text
    )


@app.post("/demo/traffic")
async def generate_traffic(requests: int = 20):
    """Fires a burst of realistic checkout requests, for demo purposes."""
    results = {"sent": 0, "ok": 0, "failed": 0}

    async def one_request(client):
        sku = random.choice(SAMPLE_SKUS)
        try:
            resp = await client.post(
                f"{CHECKOUT_URL}/checkout",
                json={"sku": sku, "quantity": random.randint(1, 3)},
                timeout=10.0,
            )
            results["sent"] += 1
            if resp.status_code < 400:
                results["ok"] += 1
            else:
                results["failed"] += 1
        except httpx.HTTPError:
            results["sent"] += 1
            results["failed"] += 1

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[one_request(client) for _ in range(requests)])

    return results
