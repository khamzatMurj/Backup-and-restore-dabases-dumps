import pymysql
from typing import List, Dict
from app.models.mysql_config import MySQLConfig

class MySQLInfoService:
    
    def get_databases_with_tables(self, config: MySQLConfig) -> List[Dict]:
        """Get all databases and their tables from MySQL server"""
        try:
            # Connect to MySQL server
            connection = pymysql.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                charset='utf8mb4'
            )
            
            databases = []
            
            with connection.cursor() as cursor:
                # Get all databases (excluding system databases)
                cursor.execute("""
                    SHOW DATABASES
                """)
                db_results = cursor.fetchall()
                
                for db_row in db_results:
                    db_name = db_row[0]
                    
                    # Skip system databases
                    if db_name in ['information_schema', 'performance_schema', 'mysql', 'sys']:
                        continue
                    
                    # Get tables for this database
                    cursor.execute(f"USE `{db_name}`")
                    cursor.execute("SHOW TABLES")
                    table_results = cursor.fetchall()
                    
                    tables = []
                    for table_row in table_results:
                        table_name = table_row[0]
                        
                        # Get table info (row count and size)
                        cursor.execute(f"""
                            SELECT 
                                table_rows as row_count,
                                ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb
                            FROM information_schema.tables 
                            WHERE table_schema = %s AND table_name = %s
                        """, (db_name, table_name))
                        
                        table_info = cursor.fetchone()
                        row_count = table_info[0] if table_info and table_info[0] else 0
                        size_mb = table_info[1] if table_info and table_info[1] else 0
                        
                        tables.append({
                            "name": table_name,
                            "row_count": row_count,
                            "size": f"{size_mb} MB"
                        })
                    
                    databases.append({
                        "name": db_name,
                        "tables": tables
                    })
            
            connection.close()
            return databases
            
        except Exception as e:
            raise Exception(f"Failed to connect to MySQL: {str(e)}")