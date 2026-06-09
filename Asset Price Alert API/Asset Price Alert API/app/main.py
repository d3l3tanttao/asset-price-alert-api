from fastapi import Depends, FastAPI
from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth.router import router as auth_router
from app.config import Settings, get_settings
from app.database import check_database_connection, get_db


app = FastAPI(
    title="Asset Price Alert API",
    description="Backend API for tracking asset prices and creating threshold-based alerts.",
    version="0.1.0",
)

app.include_router(auth_router)


@app.get("/health", tags=["System"])
def health_check(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
    }


@app.get("/db-health", tags=["System"])
def database_health_check() -> dict[str, str]:
    check_database_connection()

    return {
        "status": "ok",
        "database": "connected",
    }


@app.get("/redis-health", tags=["System"])
def redis_health_check(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    redis_client = Redis.from_url(settings.redis_url)
    redis_client.ping()

    return {
        "status": "ok",
        "redis": "connected",
    }


@app.get("/db-tables", tags=["System"])
def database_tables(db: Session = Depends(get_db)) -> dict[str, list[str]]:
    result = db.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
        )
    )

    tables = [row[0] for row in result.fetchall()]

    return {"tables": tables}
