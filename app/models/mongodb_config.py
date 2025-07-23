from pydantic import BaseModel
from typing import Optional

class MongoDBConfig(BaseModel):
    host: str
    port: int
    user: Optional[str] = None
    password: Optional[str] = None
    dbname: str
    auth_source: Optional[str] = "admin"  # Authentication database

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "host": "192.168.8.2",
                    "port": 27017,
                    "user": "root",
                    "password": "root",
                    "dbname": "db_bourse",
                    "auth_source": "admin"
                }
            ]
        }
    }

class MongoDBRestoreRequest(MongoDBConfig):
    file_path: str
    create_db_if_not_exists: bool = True  # Auto-create database option

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "host": "192.168.8.2",
                    "port": 27017,
                    "user": "root",
                    "password": "root",
                    "dbname": "db_bourse",
                    "auth_source": "admin",
                    "file_path": "/tmp/dumps/employees-mongo-dump-2025-07-23.archive",
                    "create_db_if_not_exists": True
                }
            ]
        }
    }