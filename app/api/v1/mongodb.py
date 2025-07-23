from fastapi import APIRouter, HTTPException
from app.models.mongodb_config import MongoDBConfig, MongoDBRestoreRequest
from app.services.mongodb_backup import MongoDBBackupService
from app.services.mongodb_info import MongoDBInfoService
import subprocess
import os

router = APIRouter(prefix="/mongodb", tags=["MongoDB"])
backup_service = MongoDBBackupService()
mongodb_info_service = MongoDBInfoService()

@router.post("/dump")
def create_dump(config: MongoDBConfig):
    """Create a MongoDB database dump"""
    try:
        dump_dir = backup_service.create_dump(config)
        db_subfolder = os.path.join(dump_dir, config.dbname)
        return {
            "message": "MongoDB dump created", 
            "file": db_subfolder,
            "database": config.dbname
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB dump failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.post("/restore")
def restore_dump(req: MongoDBRestoreRequest):
    """Restore a MongoDB database from dump file with auto database creation"""
    try:
        # Check if database exists before restore
        db_exists = backup_service.database_exists(req)
        
        backup_service.restore_dump(req, req.file_path)
        
        return {
            "message": "MongoDB database restored successfully",
            "database": req.dbname,
            "database_existed_before_restore": db_exists
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB restore failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.post("/databases")
def list_databases_and_collections(config: MongoDBConfig):
    """List all databases and their collections in MongoDB server"""
    try:
        result = mongodb_info_service.get_databases_with_collections(config)
        return {
            "databases": result,
            "total_databases": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch MongoDB databases: {e}")

@router.post("/check-database")
def check_database_exists(config: MongoDBConfig):
    """Check if a specific MongoDB database exists"""
    try:
        exists = backup_service.database_exists(config)
        return {
            "database": config.dbname,
            "exists": exists,
            "message": f"Database '{config.dbname}' {'exists' if exists else 'does not exist'}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check database: {e}")

@router.post("/create-database")
def create_database(config: MongoDBConfig):
    """Create a MongoDB database if it doesn't exist"""
    try:
        exists = backup_service.database_exists(config)
        if exists:
            return {
                "database": config.dbname,
                "message": f"Database '{config.dbname}' already exists",
                "created": False
            }
        
        backup_service.create_database(config)
        return {
            "database": config.dbname,
            "message": f"Database '{config.dbname}' created successfully",
            "created": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create database: {e}")