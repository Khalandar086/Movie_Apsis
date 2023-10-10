import psycopg2

from flask_login import UserMixin

DB_NAME = "login_session"
DB_USER = "postgres"
DB_PASSWORD = "Dada@12345"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"


GET_USER_BY_ID_QUERY = "SELECT * FROM USERPROFILE WHERE id=%s;"
GET_USER_BY_EMAIL_QUERY = "SELECT * FROM USERPROFILE WHERE email=%s;"


def get_db_connection():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)


class UserProfile(UserMixin):

    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def get_user_by_id(cls, id):
        conn = get_db_connection()
        curr = conn.cursor()
        if isinstance(id, str):
            id = int(id)
        curr.execute(GET_USER_BY_ID_QUERY, (id,))
        user_record = curr.fetchone()
        if user_record:
            return cls(user_record[0], user_record[1], user_record[2], user_record[3])

    @classmethod
    def get_user_by_email(cls, email):
        conn = get_db_connection()
        curr = conn.cursor()
        curr.execute(GET_USER_BY_EMAIL_QUERY, (email,))
        user_record = curr.fetchone()
        if user_record:
            return cls(user_record[0], user_record[1], user_record[2], user_record[3])
