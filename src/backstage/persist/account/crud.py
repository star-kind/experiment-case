import sys
sys.path.append('./backstage/persist/common')

import explore_tables
import execute_sentence

from app_factory import create_app
app=create_app()

def create_table():
  sentence='''CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE CHECK(length(email) <= 50),
    password TEXT NOT NULL UNIQUE CHECK(length(password) <= 200),
    salt TEXT NOT NULL UNIQUE CHECK(length(salt) <= 200),
    property INTEGER DEFAULT 0
  );'''
  execute_sentence.execute_no_result(sentence)
  explore_tables.explore_tables()
    
def inserts(email,passwd,salt):
  sentence1="INSERT INTO accounts (email,password,salt) VALUES ("
  sentence2= '"'+str(email)+'",'
  sentence3='"'+str(passwd)+'",'
  sentence4='"'+str(salt)+'");'
  sentence5=sentence1+sentence2+sentence3+sentence4
  
  create_table()
  execute_sentence.execute_no_result(sentence5)

def select_all():
  sentence="SELECT id,email,password,salt from accounts"
  results=execute_sentence.execute_fetch_records(sentence)
  
  return results
  
def select_one_by_email(email):
  create_table()
  
  sentence="SELECT id,email,password,salt from accounts"
  sentence1=' WHERE email="'+str(email)+'";'
  sentence2=sentence+sentence1
  print(sentence2)
  results=execute_sentence.execute_fetch_records(sentence2)
  
  return results
  
def select_one_by_id(id):
  sentence="SELECT id,email,password,salt from accounts"
  sentence1=' WHERE id="'+str(id)+'";'
  sentence2=sentence+sentence1
  print(sentence2)
  results=execute_sentence.execute_fetch_records(sentence2)
  
  return results  
  
def update_email_by_id(new_email,id):
  sentence="UPDATE accounts SET email = " 
  sentence1="'"+new_email+"'"
  sentence2=" WHERE id="+str(id)+";"
  sentence3=sentence+sentence1+sentence2
  
  execute_sentence.execute_no_result(sentence3)
  
def update_password_by_id(new_password,id):
  sentence="UPDATE accounts SET password = " 
  sentence1="'"+new_password+"'"
  sentence2=" WHERE id="+str(id)+";"
  sentence3=sentence+sentence1+sentence2
  
  execute_sentence.execute_no_result(sentence3)
  
def update_password_by_email(new_password,email):
  sentence="UPDATE accounts SET password = " 
  sentence1="'"+new_password+"'"
  sentence2=" WHERE email='"+str(email)+"';"
  sentence3=sentence+sentence1+sentence2
  
  execute_sentence.execute_no_result(sentence3)  
  