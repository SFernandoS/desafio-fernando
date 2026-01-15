import logging
import requests
from fastapi import FastAPI, Request, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-gateway")

app = FastAPI()


@app.get("/roll")
def roll(request: Request):
    client_host = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    logger.info(
        "incoming_request",
        extra={
            "http.client_ip": client_host,
            "http.user_agent": user_agent,
            "http.route": "/roll",
        },
    )

    try:
        resp = requests.get(
            "http://dice-service:8001/roll",
            timeout=5,
        )
        resp.raise_for_status()

    except requests.Timeout:
        logger.error(
            "dice_service_timeout",
            extra={"downstream.service": "dice-service"},
        )
        raise HTTPException(status_code=504, detail="dice-service timeout")

    except requests.RequestException as e:
        logger.error(
            "dice_service_error",
            extra={
                "downstream.service": "dice-service",
                "error.type": type(e).__name__,
            },
        )
        raise HTTPException(status_code=502, detail="dice-service error")

    logger.info(
        "dice_service_response",
        extra={
            "downstream.service": "dice-service",
            "http.status_code": resp.status_code,
        },
    )

    return resp.json()
