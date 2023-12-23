import sys
sys.path.append('./backstage/persist/common')

import execute_sentence
import explore_tables

from app_factory import create_app
app=create_app()

def create_essay_tbl():
  sentence='''CREATE TABLE IF NOT EXISTS essay (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    account_id INTEGER NOT NULL,
    account_email TEXT NOT NULL,
    modification_time TEXT NOT NULL,
    notch INTEGER NOT NULL DEFAULT 0,
    is_encrypted INTEGER NOT NULL DEFAULT 0
  );'''
  execute_sentence.execute_no_result(sentence)
  explore_tables.explore_tables()

