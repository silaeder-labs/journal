import psycopg2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from database.config import get_connection

def get_results_by_user_id(user_id):
    connection = get_connection()

    cursor = connection.cursor()

    query = "SELECT * FROM average_marks WHERE student_mesh_id = %s;"

    cursor.execute(query, (user_id,))

    records = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()

    return records

def get_columns_in_database():
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute("SELECT * FROM average_marks LIMIT 0")
    colnames = [desc[0] for desc in cur.description]

    return colnames

def get_all_users():
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute("SELECT last_name, first_name, middle_name, id FROM users")
    rows = cur.fetchall() 

    users = [f"{row[0]} {row[1]} {row[2]}" for row in rows]
    ids = [row[3] for row in rows]
    
    cur.close()
    connection.close()

    return users, ids

def marks_by_id(user_id):
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute("SELECT mesh_student_id FROM users WHERE id = %s", (user_id,))

    rows = cur.fetchone() 

    return get_results_by_user_id(rows[0])

if __name__ == "__main__":
    print(marks_by_id("1183460296"))