import psycopg2
from psycopg2 import sql
import os
import subprocess
import json
from main import get_connection

def get_subjects_info():
    node_script = os.path.join(
        BASE_DIR,
        "../exports/mesh/export_subjects.js"
    )

    result = subprocess.check_output(
        ["node", node_script],
        text=True
    )

    data = json.loads(result)

    return data["subject_ids"], data["subjects_names"]

def init_average_marks():
    conn = get_connection()
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

    cursor.execute(query)
    cursor.close()
    conn.close()

if __name__ == "main":
    init_average_marks()