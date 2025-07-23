import os
import subprocess
import datetime
from pymongo import MongoClient
from app.models.mongodb_config import MongoDBConfig

DUMP_DIR = "/tmp/dumps"
os.makedirs(DUMP_DIR, exist_ok=True)

class MongoDBBackupService:

    def _build_connection_string(self, config: MongoDBConfig) -> str:
        """Build MongoDB connection string"""
        if config.user and config.password:
            return f"mongodb://{config.user}:{config.password}@{config.host}:{config.port}/{config.dbname}?authSource={config.auth_source}"
        else:
            return f"mongodb://{config.host}:{config.port}/{config.dbname}"

    def _build_mongodump_command(self, config: MongoDBConfig, output_dir: str) -> list:
        """Build mongodump command"""
        cmd = [
            "mongodump",
            "--host", f"{config.host}:{config.port}",
            "--db", config.dbname,
            "--out", output_dir
        ]
        
        if config.user and config.password:
            cmd.extend([
                "--username", config.user,
                "--password", config.password,
                "--authenticationDatabase", config.auth_source
            ])
        
        return cmd

    def _build_mongorestore_command(self, config: MongoDBConfig, dump_path: str) -> list:
        """Build mongorestore command"""
        cmd = [
            "mongorestore",
            "--host", f"{config.host}:{config.port}",
            "--db", config.dbname,
            dump_path
        ]
        
        if config.user and config.password:
            cmd.extend([
                "--username", config.user,
                "--password", config.password,
                "--authenticationDatabase", config.auth_source
            ])
        
        return cmd

    def create_dump(self, config: MongoDBConfig) -> str:
        """Create MongoDB database dump"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        dump_name = f"{config.dbname}-mongodb-dump-{today}"
        dump_dir = os.path.join(DUMP_DIR, dump_name)
        
        # Create dump directory
        os.makedirs(dump_dir, exist_ok=True)
        
        # Build and execute mongodump command
        cmd = self._build_mongodump_command(config, dump_dir)
        subprocess.run(cmd, check=True)
        
        # Do NOT create tar archive, just return the dump directory
        return dump_dir

    def database_exists(self, config: MongoDBConfig) -> bool:
        """Check if MongoDB database exists"""
        try:
            connection_string = self._build_connection_string(config)
            client = MongoClient(connection_string)
            
            # List all databases
            db_list = client.list_database_names()
            exists = config.dbname in db_list
            
            client.close()
            return exists
        except Exception as e:
            raise Exception(f"Failed to check database existence: {str(e)}")

    def create_database(self, config: MongoDBConfig):
        """Create MongoDB database by inserting a dummy document"""
        try:
            connection_string = self._build_connection_string(config)
            client = MongoClient(connection_string)
            
            # Create database by creating a collection and inserting a document
            db = client[config.dbname]
            # Create a temporary collection to initialize the database
            temp_collection = db['_temp_init']
            temp_collection.insert_one({"init": True})
            # Remove the temporary document
            temp_collection.delete_one({"init": True})
            
            client.close()
            print(f"Database '{config.dbname}' created successfully")
        except Exception as e:
            raise Exception(f"Failed to create database: {str(e)}")

    def restore_dump(self, config: MongoDBConfig, file_path: str):
        """Restore MongoDB database from dump file with database existence check"""
        if not os.path.exists(file_path):
            raise FileNotFoundError("Dump file not found")
        
        # Check if database exists
        db_exists = self.database_exists(config)
        
        if not db_exists:
            print(f"Database '{config.dbname}' does not exist. Creating it...")
            self.create_database(config)
        else:
            print(f"Database '{config.dbname}' already exists. Proceeding with restore...")
        
        dump_path = file_path
        
        try:
            # Build and execute mongorestore command
            cmd = self._build_mongorestore_command(config, dump_path)
            subprocess.run(cmd, check=True)
            
            print(f"Database '{config.dbname}' restored successfully")
        except Exception as e:
            raise Exception(f"Failed to restore database: {e}")