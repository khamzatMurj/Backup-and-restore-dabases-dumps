import os
import subprocess
import datetime
from app.models.mysql_config import MySQLConfig
import pymysql

DUMP_DIR = "/tmp/dumps"
os.makedirs(DUMP_DIR, exist_ok=True)

class MySQLBackupService:

    def create_dump(self, config: MySQLConfig) -> str:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{config.dbname}-mysql-dump-{today}.sql"
        full_path = os.path.join(DUMP_DIR, filename)

        subprocess.run([
            "mysqldump",
            "-h", config.host,
            "-P", str(config.port),
            "-u", config.user,
            f"-p{config.password}",
            config.dbname
        ], stdout=open(full_path, 'w'), check=True)

        return full_path

    def restore_dump(self, config: MySQLConfig, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Dump file not found")

        # Check if database exists, create if not
        try:
            connection = pymysql.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                charset='utf8mb4'
            )
            with connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES LIKE %s", (config.dbname,))
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute(f'CREATE DATABASE `{config.dbname}`')
            connection.commit()
            connection.close()
        except Exception as e:
            raise Exception(f"Failed to check or create database: {e}")

        with open(file_path, 'r') as dump_file:
            subprocess.run([
                "mysql",
                "-h", config.host,
                "-P", str(config.port),
                "-u", config.user,
                f"-p{config.password}",
                config.dbname
            ], stdin=dump_file, check=True)