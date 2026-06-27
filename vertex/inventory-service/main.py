"""
Vertex Platform — Inventory Service
Checks stock availability before an order is confirmed.
"""

import asyncio
import random

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI(title="Vertex Inventory Service", version="1.0.0")
Instrumentator().instrument(app).expose(app)

_stock = {f"sku-{i}": random.randint(0, 50) for i in range(1, 21)}


class StockCheckRequest(BaseModel):
    sku: str
    quantity: int = 1


@app.get("/health")
async def health():
    return {"status": "ok", "service": "inventory-service"}


@app.get("/stock/{sku}")
async def get_stock(sku: str):
    await asyncio.sleep(random.uniform(0.01, 0.08))
    qty = _stock.get(sku)
    if qty is None:
        raise HTTPException(status_code=404, detail="SKU not found")
    return {"sku": sku, "available": qty}


@app.post("/stock/check")
async def check_stock(req: StockCheckRequest):
    await asyncio.sleep(random.uniform(0.01, 0.08))
    qty = _stock.get(req.sku, 0)
    available = qty >= req.quantity
    return {"sku": req.sku, "requested": req.quantity, "available": available}
