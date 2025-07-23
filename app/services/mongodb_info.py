from pymongo import MongoClient
from typing import List, Dict
from app.models.mongodb_config import MongoDBConfig

class MongoDBInfoService:
    
    def _build_connection_string(self, config: MongoDBConfig) -> str:
        """Build MongoDB connection string"""
        if config.user and config.password:
            return f"mongodb://{config.user}:{config.password}@{config.host}:{config.port}/?authSource={config.auth_source}"
        else:
            return f"mongodb://{config.host}:{config.port}/"

    def get_databases_with_collections(self, config: MongoDBConfig) -> List[Dict]:
        """Get all databases and their collections from MongoDB server"""
        try:
            connection_string = self._build_connection_string(config)
            client = MongoClient(connection_string)
            
            databases = []
            
            # Get all databases (excluding system databases)
            db_list = client.list_database_names()
            
            for db_name in db_list:
                # Skip system databases
                if db_name in ['admin', 'config', 'local']:
                    continue
                
                db = client[db_name]
                collection_names = db.list_collection_names()
                
                collections = []
                for collection_name in collection_names:
                    collection = db[collection_name]
                    
                    # Get collection stats
                    try:
                        stats = db.command("collStats", collection_name)
                        doc_count = stats.get('count', 0)
                        size_bytes = stats.get('size', 0)
                        size_mb = round(size_bytes / 1024 / 1024, 2)
                    except Exception:
                        # If collStats fails, use estimated count
                        doc_count = collection.estimated_document_count()
                        size_mb = 0
                    
                    collections.append({
                        "name": collection_name,
                        "document_count": doc_count,
                        "size": f"{size_mb} MB"
                    })
                
                # Get database stats
                try:
                    db_stats = db.command("dbStats")
                    db_size_mb = round(db_stats.get('dataSize', 0) / 1024 / 1024, 2)
                except Exception:
                    db_size_mb = sum(float(col['size'].replace(' MB', '')) for col in collections)
                
                databases.append({
                    "name": db_name,
                    "size": f"{db_size_mb} MB",
                    "collections": collections
                })
            
            client.close()
            return databases
            
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")