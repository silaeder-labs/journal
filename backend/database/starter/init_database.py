import psycopg2
from psycopg2 import sql
from starter import BASE_DIR, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def init_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", [DB_NAME])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))

    cursor.close()
    conn.close()

if __name__ == "main":
    init_database()