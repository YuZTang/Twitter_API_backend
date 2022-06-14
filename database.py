import psycopg2
from psycopg2 import pool


def connect():
    return psycopg2.connect(user="postgres",database="learning",host="localhost")

# connection_pool = psycopg2.pool.SimpleConnectionPool(1,10,user="postgres",database="learning",host="localhost")

# connection_pool2 = pool.SimpleConnectionPool(1,10,user="postgres",database="learning",host="localhost")

class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,10,**kwargs)

    @classmethod
    def get_connection(cls):
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        return Database.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()


class ConnectionPool:
    def __init__(self) -> None:
        self.connection_pool = pool.SimpleConnectionPool(1,1,user="postgres",database="learning",host="localhost")

    def __enter__(self):
        return self.connection_pool.getconn()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class CursorFromConnectionFromPool:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)

     