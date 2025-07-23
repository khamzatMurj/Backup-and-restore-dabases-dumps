import psycopg2
from psycopg2.extras import RealDictCursor
from app.models.db_config import DBConfig
from app.models.database_info import DatabaseInfo, TableInfo

class PostgresInfoService:
    def get_databases_with_tables(self, config: DBConfig) -> list:
        # Connexion à la base postgres pour lister les bases
        db_list = []
        try:
            conn = psycopg2.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                dbname='postgres'
            )
            conn.autocommit = True
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                databases = [row['datname'] for row in cur.fetchall()]
            conn.close()
        except Exception as e:
            raise Exception(f"Erreur lors de la connexion à postgres: {e}")

        # Pour chaque base, lister les tables et infos
        for db in databases:
            try:
                db_conn = psycopg2.connect(
                    host=config.host,
                    port=config.port,
                    user=config.user,
                    password=config.password,
                    dbname=db
                )
                with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT tablename FROM pg_tables WHERE schemaname = 'public';
                    """)
                    tables = [row['tablename'] for row in cur.fetchall()]
                    table_infos = []
                    for table in tables:
                        # Nombre de lignes
                        cur.execute(f"SELECT COUNT(*) as row_count FROM \"{table}\";")
                        row_count = cur.fetchone()['row_count']
                        # Taille
                        cur.execute(f"SELECT pg_size_pretty(pg_total_relation_size(\"{table}\")) as size;")
                        size = cur.fetchone()['size']
                        table_infos.append(TableInfo(name=table, row_count=row_count, size=size))
                db_conn.close()
                db_list.append(DatabaseInfo(name=db, tables=table_infos))
            except Exception as e:
                # Si une base n'est pas accessible, on continue
                continue
        return [db.model_dump() for db in db_list] 