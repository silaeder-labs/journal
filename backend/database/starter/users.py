import psycopg2
from psycopg2 import sql
from starter import BASE_DIR, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def init_users():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    users_columns = {
        "id": "INT UNIQUE PRIMARY KEY",
        "mesh_student_id": "TEXT",
        "class": "INT",
        "first_name": "TEXT",
        "last_name": "TEXT",
        "middle_name": "TEXT",
        "keycloack_user_id": "TEXT UNIQUE"
    }

    query = sql.SQL("CREATE TABLE IF NOT EXISTS users ({fields})").format(
        fields=sql.SQL(", ").join(
            sql.SQL("{} {}").format(
                sql.Identifier(name),
                sql.SQL(col_type)
            )
            for name, col_type in users_columns.items()
        )
    )

    cursor.execute(query)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_users()