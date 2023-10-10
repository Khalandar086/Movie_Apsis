import psycopg2


class PG_CONN:

    conn = None
    DB_NAME = "user_registration_db"
    DB_USER = "postgres"
    DB_PASSWORD = "Dada@12345"
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"

    @classmethod
    def get_db_connection(cls):
        cls.conn = psycopg2.connect(dbname=cls.DB_NAME, user=cls.DB_USER, password=cls.DB_PASSWORD)
        return cls.conn

conn=PG_CONN.get_db_connection()