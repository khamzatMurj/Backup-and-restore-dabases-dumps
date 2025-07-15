from fastapi import APIRouter, HTTPException
from app.models.db_config import DBConfig
from app.services.backup import BackupService
import subprocess

router = APIRouter()
backup_service = BackupService()

@router.post("/dump")
def create_dump(config: DBConfig):
    try:
        file_path = backup_service.create_dump(config)
        return {"message": "Dump created", "file": file_path}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Dump failed: {e}")
