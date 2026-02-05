import psycopg2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from database.config import get_connection

# =====COLUMNS=====

def get_table_columns(table: str):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"SELECT * FROM { table } LIMIT 0"

    cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]

    if connection:
        cursor.close()
        connection.close()

    return columns

# =====USERS_INFO=====

def get_all_students_info() -> list[list[int, int, str, str, str]]:
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT class, id, last_name, first_name, middle_name FROM users"

    cursor.execute(query)

    users_info = [list(row) for row in cursor.fetchall()]

    if connection:
        cursor.close()
        connection.close()

    return users_info

# =====MARKS=====

def get_student_marks_by_mesh_id(mesh_student_id: str) -> list[float |  None]:
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM average_marks WHERE mesh_student_id = %s"

    cursor.execute(query, (mesh_student_id,))

    marks = cursor.fetchone()

    if connection:
        cursor.close()
        connection.close()

    return marks

# =====SKILLS=====

def get_student_skills_by_id(user_id: int) -> list[int]:
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM skills WHERE id = %s"

    cursor.execute(query, (user_id,))

    skills = cursor.fetchone()

    if connection:
        cursor.close()
        connection.close()

    return skills

# =====CONVERTORS=====

def convert_from_mesh_id_to_normal_id(mesh_student_id: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT id FROM users WHERE mesh_student_id = %s"

    cursor.execute(query, (mesh_student_id,))

    id = cursor.fetchone()

    if connection:
        cursor.close()
        connection.close()

    return id[0]

def convert_from_normal_id_to_mesh_id(user_id: int) -> str:
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT mesh_student_id FROM users WHERE id = %s"

    cursor.execute(query, (user_id,))

    mesh_id = cursor.fetchone()

    if connection:
        cursor.close()
        connection.close()

    return mesh_id[0]


# =====TESTS=====

if __name__ == "__main__":
    print(get_student_marks_by_mesh_id("0799482a-f4b8-44fb-a087-f1d25c6753ea"))
    print(convert_from_mesh_id_to_normal_id("0799482a-f4b8-44fb-a087-f1d25c6753ea"))
    print(convert_from_normal_id_to_mesh_id(1750700615))
    print(get_all_students_info())
    print(get_table_columns("average_marks"))
    print(get_student_skills_by_id(724214433))