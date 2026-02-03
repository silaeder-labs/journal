import psycopg2
from psycopg2 import sql
from starter import get_connection

def init_database():
    conn = get_connection()
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