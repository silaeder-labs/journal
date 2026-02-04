from psycopg2 import sql
import psycopg2
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_connection

def main():
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    try:
        ids = []

        cur.execute("SELECT id FROM users")
        records = cur.fetchall()

        for record in records:
            id = record[0]
            ids.append(id)

        for id in ids:
            cur.execute(
                "INSERT INTO skills (id) VALUES (%s) ON CONFLICT (id) DO NOTHING", 
                (id,)
            )
            
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
