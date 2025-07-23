from fastapi import FastAPI
from app.api.v1 import postgres
from app.api.v1 import mysql, mongodb

app = FastAPI(title="Multi-Database Backup API")

app.include_router(postgres.router, prefix="/api/v1")

# Future database routers
app.include_router(mongodb.router, prefix="/api/v1")

# MySQL routes (new)
app.include_router(mysql.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Multi-Database Backup API", 
        "supported_databases": ["PostgreSQL", "MySQL", "MongoDB"],
        "endpoints": {
            "postgresql": {
                "dump": "/api/v1/dump",
                "restore": "/api/v1/restore"
            },
            "mysql": {
                "dump": "/api/v1/mysql/dump",
                "restore": "/api/v1/mysql/restore",
                "databases": "/api/v1/mysql/databases"
            },
            "mongodb": {
                "dump": "/api/v1/mongodb/dump",
                "restore": "/api/v1/mongodb/restore",
                "databases": "/api/v1/mongodb/databases",
                "check-database": "/api/v1/mongodb/check-database",
                "create-database": "/api/v1/mongodb/create-database"
            }
        }
    }