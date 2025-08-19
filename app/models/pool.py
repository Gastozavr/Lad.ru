import psycopg2
import config
from psycopg2 import pool

class DatabasePool:
    def __init__(self):
        self.pool = None
    
    def create_pool(self):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            host=config.pg_url,
            database=config.pg_db,
            user=config.pg_username,
            password=config.pg_password
        )
        
        if self.pool:
            print("Пул соединений создан успешно")
            return True
        return False
    
    def getconn(self):
        return self.pool.getconn()
    
    def putconn(self, conn):
        self.pool.putconn(conn)

db_pool = DatabasePool()