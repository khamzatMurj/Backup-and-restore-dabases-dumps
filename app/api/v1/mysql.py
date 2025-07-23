from fastapi import APIRouter, HTTPException
from app.models.mysql_config import MySQLConfig, MySQLRestoreRequest
from app.services.mysql_backup import MySQLBackupService
from app.services.mysql_info import MySQLInfoService
import subprocess

router = APIRouter(prefix="/mysql", tags=["MySQL"])
backup_service = MySQLBackupService()
mysql_info_service = MySQLInfoService()

@router.post("/dump")
def create_dump(config: MySQLConfig):
    """Create a MySQL database dump"""
    try:
        file_path = backup_service.create_dump(config)
        return {"message": "MySQL dump created", "file": file_path}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"MySQL dump failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.post("/restore")
def restore_dump(req: MySQLRestoreRequest):
    try:
        backup_service.restore_dump(req, req.file_path)
        return {"message": "MySQL database restored"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # This will catch both DB creation and restore errors
        raise HTTPException(status_code=500, detail=f"MySQL restore failed: {e}")

@router.post("/databases")
def list_databases_and_tables(config: MySQLConfig):
    """List all databases and their tables in MySQL server"""
    try:
        result = mysql_info_service.get_databases_with_tables(config)
        return {"databases": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch MySQL databases: {e}")