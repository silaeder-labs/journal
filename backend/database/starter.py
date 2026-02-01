import psycopg2
from psycopg2 import sql
import subprocess
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_subjects_info():
    node_script = os.path.join(
        BASE_DIR,
        "export_subjects.js"
    )

    result = subprocess.check_output(
        ["node", node_script],
        text=True
    )

    data = json.loads(result)

    return data["subject_ids"], data["subjects_names"]


DB_NAME = "marks"
DB_USER = "test_superuser"
DB_PASSWORD = "passwords"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

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

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cursor = conn.cursor()

subjects_data = get_subjects_info()

#таблица средних оценок где для обозначения ученика используется его МЭШ id
average_marks_columns = {
    "student_mesh_id": "TEXT UNIQUE PRIMARY KEY",
}

for i in range(len(subjects_data[1])):
    average_marks_columns[str(subjects_data[1][i])] = "FLOAT"

query = sql.SQL("CREATE TABLE IF NOT EXISTS average_marks ({fields})").format(
    fields=sql.SQL(", ").join(
        sql.SQL("{} {}").format(
            sql.Identifier(name),
            sql.SQL(col_type)
        )
        for name, col_type in average_marks_columns.items()
    )
)

users_columns = {
    "id": "INT UNIQUE PRIMARY KEY",
    "mesh_student_id": "TEXT UNIQUE",
    "class": "INT",
    "first_name": "TEXT",
    "last_name": "TEXT",
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
