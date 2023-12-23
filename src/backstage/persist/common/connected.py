import os
import sqlite3
from app_factory import create_app

app=create_app()

def connect_database():
  print(__name__,' app.config.DB_FILE_PATH: ', app.config['DB_FILE_PATH'])
  db_name=app.config['DB_FILE_PATH']
  
  if not os.path.exists(db_name):
    conn = sqlite3.connect(db_name)
    print(__name__,'.class=',f"database: {db_name} had created")
  else:
    conn = sqlite3.connect(db_name)
    print(__name__,'.class=',f"connected to database: {db_name}")
  return conn

