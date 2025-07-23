import os
import subprocess
import datetime
from app.models.db_config import DBConfig
import psycopg2

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

        # Check if database exists, create if not
        try:
            conn = psycopg2.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                dbname='postgres'
            )
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (config.dbname,))
                exists = cur.fetchone()
                if not exists:
                    cur.execute(f'CREATE DATABASE "{config.dbname}"')
            conn.close()
        except Exception as e:
            raise Exception(f"Failed to check or create database: {e}")

        with open(file_path, 'r') as dump_file:
            subprocess.run([
                "psql",
                "-h", config.host,
                "-p", str(config.port),
                "-U", config.user,
                "-d", config.dbname
            ], stdin=dump_file, check=True, env={**os.environ, "PGPASSWORD": config.password})
