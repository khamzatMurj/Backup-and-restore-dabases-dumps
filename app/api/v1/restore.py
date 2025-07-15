from fastapi import APIRouter, HTTPException
from app.models.db_config import RestoreRequest
from app.services.backup import BackupService
import subprocess

router = APIRouter()
backup_service = BackupService()

@router.post("/restore")
def restore_dump(req: RestoreRequest):
    try:
        backup_service.restore_dump(req, req.file_path)
        return {"message": "Database restored"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {e}")
