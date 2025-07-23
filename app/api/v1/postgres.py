from fastapi import APIRouter, HTTPException
from app.models.db_config import DBConfig, RestoreRequest
from app.services.backup import BackupService
from app.services.postgres_info import PostgresInfoService
import subprocess

router = APIRouter(prefix="/postgres", tags=["PostgreSQL"])
backup_service = BackupService()
postgres_info_service = PostgresInfoService()

@router.post("/dump")
def create_dump(config: DBConfig):
    try:
        file_path = backup_service.create_dump(config)
        return {"message": "Dump created", "file": file_path}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Dump failed: {e}")

@router.post("/restore")
def restore_dump(req: RestoreRequest):
    try:
        backup_service.restore_dump(req.config, req.file_path)
        return {"message": "Restore successful"}
    except Exception as e:
        # This will catch both DB creation and restore errors
        raise HTTPException(status_code=500, detail=f"Restore failed: {e}")

@router.post("/databases")
def list_databases_and_tables(config: DBConfig):
    try:
        result = postgres_info_service.get_databases_with_tables(config)
        return {"databases": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch databases: {e}") 