
import psycopg2


class PG_CONN:

    conn = None
    DB_NAME = "move_db"
    DB_USER = "postgres"
    DB_PASSWORD = "Dada@12345"
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"

    @classmethod
    def get_db_connection(cls):
        cls.conn = psycopg2.connect(dbname=cls.DB_NAME, user=cls.DB_USER, password=cls.DB_PASSWORD)
        return cls.conn

try:
    conn = PG_CONN.get_db_connection()
    schema = open("schema.sql").read()
    cur = conn.cursor()
    #cur.execute("Create Database movie_db;")
    #conn.commit()
    #conn.close()
    cur.execute(schema)
    conn.commit()
except Exception as e:
    print(f"Error while executing the schema {e}")


