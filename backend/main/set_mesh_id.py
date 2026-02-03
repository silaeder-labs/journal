import psycopg2
from psycopg2 import sql
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from database.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def set_mesh_id_to_database(value, user_id):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    conn.autocommit = True
    cursor = conn.cursor()

    sql_query = "UPDATE users SET mesh_student_id = %s WHERE keycloack_user_id = %s;"

    cursor.execute(sql_query, (value, user_id))

    conn.commit()
    cursor.close()


if __name__ == "__main__":
    set_mesh_id_to_database("test", "07485d7d-fcc2-47df-bb20-a2631483ac34")