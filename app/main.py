from fastapi import FastAPI
from app.api.v1 import postgres

app = FastAPI(title="Multi-Database Backup API")

app.include_router(postgres.router, prefix="/api/v1")
# Future database routers
# app.include_router(mysql.router, prefix="/api/v1")
# app.include_router(mongodb.router, prefix="/api/v1")
