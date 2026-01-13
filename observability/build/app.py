import os
import logging
from random import randint
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Info

APP_NAME = "dice-api"


def create_app() -> FastAPI:
    app = FastAPI()

    configure_logging()

    # Instrumentação Prometheus
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)

    # Info metric equivalente
    info = Info("app_info", "Application info")
    info.info({"version": os.getenv("APP_VERSION", "dev")})

    register_routes(app)
    register_error_handlers(app)

    return app


def configure_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def register_routes(app: FastAPI) -> None:
    logger = logging.getLogger(APP_NAME)

    @app.get("/")
    async def roll_dice() -> Dict[str, int]:
        dice_value = randint(1, 6)
        logger.info(
            "Dice rolled",
            extra={"dice_value": dice_value, "app": APP_NAME},
        )
        return {"dice_value": dice_value}

    @app.get("/health")
    async def health() -> Dict[str, str]:
        return {
            "status": "ok",
            "app": APP_NAME,
            "version": os.getenv("APP_VERSION", "dev"),
        }

    @app.get("/fail")
    async def fail():
        raise RuntimeError("Intentional failure")


def register_error_handlers(app: FastAPI) -> None:
    logger = logging.getLogger(APP_NAME)

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, error: Exception):
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "app": APP_NAME,
                "message": str(error),
            },
        )


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )
