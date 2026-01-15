import asyncio
import random
import logging
import time
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("storage-service")

app = FastAPI()
sem = asyncio.Semaphore(3)


@app.post("/store")
async def store(payload: dict):
    start = time.time()
    value = payload.get("value", "unknown")

    logger.info(
        "store_request_received",
        extra={
            "storage.value": value,
            "storage.queue_size": sem._value,
        },
    )

    async with sem:
        wait_time = time.time() - start

        logger.info(
            "storage_acquired",
            extra={
                "storage.wait_time": round(wait_time, 3),
                "storage.value": value,
            },
        )

        await asyncio.sleep(1)

        if random.random() < 0.6:
            logger.error(
                "storage_timeout",
                extra={
                    "storage.value": value,
                    "storage.wait_time": round(wait_time, 3),
                },
            )
            raise HTTPException(status_code=503, detail="storage_timeout")

        elapsed = time.time() - start

        logger.info(
            "value_stored",
            extra={
                "storage.value": value,
                "storage.elapsed": round(elapsed, 3),
                "storage.wait_time": round(wait_time, 3),
            },
        )

        return {"status": "ok"}
