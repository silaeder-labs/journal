from psycopg2 import sql
import psycopg2
import get_marks as gm

DB_CONFIG = {
    "dbname": "marks",
    "user": "test_superuser",
    "password": "password",
    "host": "127.0.0.1",
    "port": 5432
}

def main():
    std_marks = gm.get_students_marks()

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        for student_id, subjects in std_marks.items():
            columns = ["student_mesh_id"]
            values = [student_id]
            
            for subject, mark in subjects.items():
                columns.append(subject)
                values.append(mark)

            update_fragments = [
                sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(col), sql.Identifier(col))
                for col in columns if col != "student_mesh_id"
            ]

            query = sql.SQL("""
                INSERT INTO average_marks ({fields})
                VALUES ({placeholders})
                ON CONFLICT (student_mesh_id)
                DO UPDATE SET {updates}
            """).format(
                fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
                updates=sql.SQL(", ").join(update_fragments)
            )

            cur.execute(query, values)
            
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
