from psycopg2 import sql
import psycopg2
import get_marks as gm

# Параметры подключения
DB_CONFIG = {
    "dbname": "marks",
    "user": "test_superuser",
    "password": "password",
    "host": "127.0.0.1",
    "port": 5432
}

def main():
    std_marks = gm.get_students_marks()

    for student in std_marks:
        values = []
        columns = ["student_mesh_id"]
        values.append(student)

        for subject in std_marks[student]:
            columns.append(subject)
            values.append(std_marks[student][subject])

        query = sql.SQL("""
            INSERT INTO average_marks ({fields})
            VALUES ({placeholders})
        """).format(
            fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns))
        )

        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(query, values)

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
