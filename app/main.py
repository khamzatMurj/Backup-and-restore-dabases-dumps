from fastapi import FastAPI
from app.api.v1 import dump, restore

app = FastAPI(title="Postgres Backup API")

app.include_router(dump.router, prefix="/api/v1")
app.include_router(restore.router, prefix="/api/v1")
