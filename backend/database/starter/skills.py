import psycopg2
from psycopg2 import sql
from starter import get_connection

def init_skills():
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    skills_columns = {
        "id": "INT UNIQUE PRIMARY KEY",
        "math": "INT",
        "IT": "INT",
        "backend": "INT",
        "frontend": "INT",
        "ML": "INT",
        "physics": "INT",
        "russian": "INT",
        "english": "INT"
    }

    query = sql.SQL("CREATE TABLE IF NOT EXISTS skills ({fields})").format(
        fields=sql.SQL(", ").join(
            sql.SQL("{} {}").format(
                sql.Identifier(name),
                sql.SQL(col_type)
            )
            for name, col_type in skills_columns.items()
        )
    )

    cursor.execute(query)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_skills()