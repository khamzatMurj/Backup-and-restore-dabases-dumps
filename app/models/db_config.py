from pydantic import BaseModel

class DBConfig(BaseModel):
    host: str
    port: int
    user: str
    dbname: str
    password: str

class RestoreRequest(DBConfig):
    file_path: str
