import psycopg2
from psycopg2 import sql

DB_NAME = "marks"
DB_USER = "test_superuser"
DB_PASSWORD = "password"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

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