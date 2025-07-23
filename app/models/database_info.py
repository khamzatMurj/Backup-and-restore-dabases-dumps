from pydantic import BaseModel
from typing import List

class TableInfo(BaseModel):
    name: str
    row_count: int
    size: str

class DatabaseInfo(BaseModel):
    name: str
    tables: List[TableInfo]

class DatabaseListResponse(BaseModel):
    databases: List[DatabaseInfo] 