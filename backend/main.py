
import os
import sqlite3
from contextlib import asynccontextmanager, closing

from fastapi import FastAPI, HTTPException

from database import get_connection, initialize_database


@asynccontextmanager
async def lifespan(app):
    initialize_database()

    app.state.key_pool = [
        key.strip()
        for key in os.getenv("LLM_API_KEYS", "").split(",")
        if key.strip()
    ]

    app.state.cache_enabled = False
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    try:
        with closing(get_connection()) as connection:
            connection.execute(
                "SELECT 1 FROM messages LIMIT 1"
            ).fetchone()
    except sqlite3.Error:
        raise HTTPException(
            status_code=503,
            detail="database unavailable",
        )

    if len(app.state.key_pool) < 2:
        raise HTTPException(
            status_code=503,
            detail="LLM key pool not configured",
        )

    return {
        "status": "ok",
        "keys_configured": len(app.state.key_pool),
        "cache_enabled": app.state.cache_enabled,
    }