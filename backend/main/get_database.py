import psycopg2

def get_results_by_user_id(user_id):
    connection = psycopg2.connect(
        user="test_superuser",
        password="password",
        host="127.0.0.1",
        port="5432",
        database="marks"
    )

    cursor = connection.cursor()

    query = "SELECT * FROM average_marks WHERE student_mesh_id = %s;"

    cursor.execute(query, (user_id,))

    records = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()

    return records

def get_columns_in_database():
    connection = psycopg2.connect(
        user="test_superuser",
        password="password",
        host="127.0.0.1",
        port="5432",
        database="marks"
    )
    
    cur = connection.cursor()

    cur.execute("SELECT * FROM average_marks LIMIT 0")
    colnames = [desc[0] for desc in cur.description]

    return colnames
