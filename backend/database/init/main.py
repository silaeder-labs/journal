import psycopg2
from psycopg2 import sql
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_connection


def init_all():
    from init_database import init_database
    from skills import init_skills
    from average_marks import init_average_marks
    from users import init_users

    try: 
        init_database()
    except Exception as e:
        print("database initialization failed")
        print(e)
        return

    try:
        init_skills()
    except Exception as e:
        print("skills initialization failed")
        print(e)

    try: 
        init_users()
    except Exception as e:
        print("users initialization failed")
        print(e)

    try: 
        init_average_marks()
    except Exception as e:
        print("average marks initialization failed")
        print(e)


if __name__ == "__main__":
    init_all()
