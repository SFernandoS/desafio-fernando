import logging
import requests
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dice-service")

app = FastAPI()


@app.get("/roll")
def roll():
    try:
        rand_resp = requests.get(
            "http://random-service:8002/random",
            timeout=5,
        )
        rand_resp.raise_for_status()
        value = rand_resp.json()["value"]

    except requests.Timeout:
        logger.error(
            "random_service_timeout",
            extra={"downstream.service": "random-service"},
        )
        raise HTTPException(status_code=504, detail="random-service timeout")

    except Exception as e:
        logger.error(
            "random_service_error",
            extra={
                "downstream.service": "random-service",
                "error.type": type(e).__name__,
            },
        )
        raise HTTPException(status_code=502, detail="random-service error")

    try:
        rules_resp = requests.post(
            "http://rules-service:8003/validate",
            json={"value": value},
            timeout=5,
        )
        rules_resp.raise_for_status()
        allowed = rules_resp.json()["allowed"]

    except requests.Timeout:
        logger.error(
            "rules_service_timeout",
            extra={
                "downstream.service": "rules-service",
                "dice.value": value,
            },
        )
        raise HTTPException(status_code=504, detail="rules-service timeout")

    except Exception as e:
        logger.error(
            "rules_service_error",
            extra={
                "downstream.service": "rules-service",
                "dice.value": value,
                "error.type": type(e).__name__,
            },
        )
        raise HTTPException(status_code=502, detail="rules-service error")

    if allowed:
        try:
            requests.post(
                "http://storage-service:8004/store",
                json={"value": value},
                timeout=5,
            ).raise_for_status()

        except requests.Timeout:
            logger.error(
                "storage_service_timeout",
                extra={
                    "downstream.service": "storage-service",
                    "dice.value": value,
                },
            )
            raise HTTPException(status_code=504, detail="storage-service timeout")

        except Exception as e:
            logger.error(
                "storage_service_error",
                extra={
                    "downstream.service": "storage-service",
                    "dice.value": value,
                    "error.type": type(e).__name__,
                },
            )
            raise HTTPException(status_code=502, detail="storage-service error")

    logger.info(
        "dice_processed",
        extra={
            "dice.value": value,
            "dice.allowed": allowed,
        },
    )

    return {"dice": value, "allowed": allowed}
