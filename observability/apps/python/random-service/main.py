import random
import time
import logging
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("random-service")

app = FastAPI()


@app.get("/random")
def random_value():
    start = time.time()

    delay = random.uniform(0.2, 1.2)
    time.sleep(delay)

    if random.random() < 0.7:
        logger.error(
            "random_generation_failed",
            extra={"random.delay": round(delay, 3)},
        )
        raise HTTPException(status_code=500, detail="random failure")

    value = random.randint(1, 6)
    elapsed = time.time() - start

    logger.info(
        "random_generated",
        extra={
            "random.value": value,
            "random.delay": round(delay, 3),
            "random.elapsed": round(elapsed, 3),
        },
    )

    return {"value": value}
