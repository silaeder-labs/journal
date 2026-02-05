import psycopg2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from database.config import get_connection

def get_results_by_user_mesh_id(user_id, table_name):
    connection = get_connection()

    cursor = connection.cursor()

    query = f"SELECT * FROM { table_name } WHERE student_mesh_id = %s;"

    cursor.execute(query, (user_id,))

    records = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()

    return records


def get_mesh_id_by_keycloak_id(keycloak_user_id):
    connection = get_connection()

    cur = connection.cursor()
    cur.execute("SELECT mesh_student_id FROM users WHERE keycloack_user_id = %s", (keycloak_user_id,))

    result = cur.fetchone()

    connection.close()

    return result[0]

def get_results_by_user_id(user_id, table_name):
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute("SELECT id FROM users WHERE mesh_student_id = %s", (user_id,))

    rows = cur.fetchone()

    cursor = connection.cursor()

    query = f"SELECT * FROM { table_name } WHERE id = %s;"

    cursor.execute(query, (rows[0],))

    records = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()

    return records

def get_marks_by_user_id(user_id):
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute("SELECT id FROM users WHERE mesh_student_id = %s", (user_id,))

    rows = cur.fetchone()

    cursor = connection.cursor()

    query = f"SELECT * FROM { table_name } WHERE id = %s;"

    cursor.execute(query, (rows[0],))

    records = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()

    return records


def get_columns_in_database(table_name):
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute(f"SELECT * FROM { table_name } LIMIT 0")
    colnames = [desc[0] for desc in cur.description]

    return colnames

def get_all_users():
    connection = get_connection()
    
    cur = connection.cursor()

    cur.execute("SELECT last_name, first_name, middle_name, id, class FROM users")
    rows = cur.fetchall() 

    users = [f"{row[0]} {row[1]} {row[2]}" for row in rows]
    ids = [row[3] for row in rows]
    classes = [row[4] for row in rows]
    
    cur.close()
    connection.close()

    return users, ids, classes

def data_by_id(user_id, table_name):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"SELECT * FROM { table_name } WHERE student_mesh_id = %s;"

    cursor.execute(query, (user_id,))

    records = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()

    return records

if __name__ == "__main__":
    print(get_results_by_user_id("769221691", "skills"))