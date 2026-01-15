import logging
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rules-service")

app = FastAPI()


@app.post("/validate")
def validate(payload: dict):
    if "value" not in payload:
        logger.error(
            "invalid_payload",
            extra={"rules.reason": "missing_value"},
        )
        raise HTTPException(status_code=400, detail="missing value")

    value = payload["value"]
    allowed = value <= 6

    logger.info(
        "rule_evaluated",
        extra={
            "rules.input.value": value,
            "rules.allowed": allowed,
            "rules.rule": "value <= 6",
        },
    )

    return {"allowed": allowed}
