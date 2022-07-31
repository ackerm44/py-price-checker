import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv

load_dotenv('.env')


def create_connection(db_file=os.environ.get("DB_FILE_PATH")):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()


