import os
import subprocess
import datetime
from app.models.db_config import DBConfig

DUMP_DIR = "/tmp/dumps"
os.makedirs(DUMP_DIR, exist_ok=True)

class BackupService:

    def create_dump(self, config: DBConfig) -> str:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{config.dbname}-dump-{today}.sql"
        full_path = os.path.join(DUMP_DIR, filename)

        subprocess.run([
            "pg_dump",
            "-h", config.host,
            "-p", str(config.port),
            "-U", config.user,
            "-d", config.dbname,
            "-f", full_path
        ], check=True, env={**os.environ, "PGPASSWORD": config.password})

        return full_path

    def restore_dump(self, config: DBConfig, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Dump file not found")

        with open(file_path, 'r') as dump_file:
            subprocess.run([
                "psql",
                "-h", config.host,
                "-p", str(config.port),
                "-U", config.user,
                "-d", config.dbname
            ], stdin=dump_file, check=True, env={**os.environ, "PGPASSWORD": config.password})
