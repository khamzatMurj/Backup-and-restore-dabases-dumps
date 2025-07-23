from pydantic import BaseModel

class MySQLConfig(BaseModel):
    host: str
    port: int
    user: str
    dbname: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "host": "localhost",
                    "port": 3306,
                    "user": "root",
                    "dbname": "employees",
                    "password": "root"
                }
            ]
        }
    }

class MySQLRestoreRequest(MySQLConfig):
    file_path: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "host": "localhost",
                    "port": 3306,
                    "user": "root",
                    "dbname": "employees",
                    "password": "root",
                    "file_path": "/tmp/dumps/employees-mysql-dump-2025-07-23.sql"
                }
            ]
        }
    }