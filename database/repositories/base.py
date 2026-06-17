from database.connection import pool


class BaseRepository:
    
    def get_pool_connection(self):
        
        connection = pool.connection()
        cursor = connection.cursor()
                
        return connection, cursor