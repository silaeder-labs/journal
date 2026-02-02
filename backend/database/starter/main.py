import psycopg2
from psycopg2 import sql
import subprocess
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = "marks"
DB_USER = "test_superuser"
DB_PASSWORD = "password"
DB_HOST = "127.0.0.1"
DB_PORT = 5432


def init_all():
    from init_database import init_database
    from skills import init_skills
    from average_marks import init_average_marks
    from users import init_users

    try: 
        init_database()
    except:
        print("database initialization failed")
        return

    try:
        init_skills()
    except:
        print("skills initialization failed")

    try: 
        init_users()
    except:
        print("users initialization failed")

    try: 
        init_average_marks()
    except:
        print("average marks initialization failed")


if __name__ == "__main__":
    init_all()
