import os
import sqlite3
import public_platform


def connect_database():
    print("connect_database.DB_FILE_PATH:", public_platform.DATABASE_PATH)
    db_name = public_platform.DATABASE_PATH

    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        print(
            f"connect_database.database before not exist: {db_name} will be create now"
        )
    else:
        conn = sqlite3.connect(db_name)
        print(f"connect_database.connected to database: {db_name} has already exist")
    return conn
