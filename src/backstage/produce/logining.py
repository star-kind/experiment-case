import sys
sys.path.append('./backstage/logger')
sys.path.append('./backstage/consts')
sys.path.append('./backstage/persist')

from flask import render_template
import re

import records
from state_consts import StateConstants
import crud
import cryptography
import token_service

def index_page():
  html_path="account/index.html"
  return render_template(html_path)

def handle_login_data(request_data):
  records.type_msg(handle_login_data_request_dataForm=request_data.form)
  return early_verify(request_data)

def early_verify(request_data):
    email=request_data.form['email']
    password=request_data.form['password']
    illegal_chars=['“', '‘', "'", '"', '~', '!', '#', '$', '%', '^', '&', '(', ')', '*', '+', '=', '[', ']', ';', ':', '\\', '/', '<', '>', ',','，','。']
      
    if len(dict(request_data.form)) == 0:
      return StateConstants.param_empty()
      
    elif any(' ' in str(s) for s in [email, password]):
      return StateConstants.contains_spaces()
      
    elif len(str(email)) > 40:
      return StateConstants.email_out_limit()
      
    elif len(str(password)) > 16:
      return StateConstants.password_out_limit()
      
    elif len(str(password)) < 4:
      return StateConstants.password_less_length()
      
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", str(email)):
      return StateConstants.invalid_email()
      
    elif any(c in str(email) for c in illegal_chars):
      return StateConstants.illegal_char()
  
    return login_check(email,password) 
      
def login_check(email,commit_password):  
  usr_list=crud.select_one_by_email(email)
  print(__name__,'  :usr_list= ',usr_list)
  
  if len(usr_list) == 0:
    # 检查是否有此账户
    return StateConstants.no_such_user()

  if kwd_pair(usr_list,commit_password) < 0:
    return StateConstants.password_incorrect() # 密码错误
  
  print(__name__,'.login_check.usr_list: ',usr_list)
  id=usr_list[0][0]
  
  response=generate_response(email,id)
  return response 

def kwd_pair(usr_list,commit_password):
  for user in usr_list:
    print("Current user:")
    for index, element in enumerate(user):
        print(f"Index: {index}, Value: {element}")
  print("\n")  

  cipher_txt=usr_list[0][2]
  private_salt=usr_list[0][3]
  
  local_kwd = cryptography.aes_decrypt(private_salt,cipher_txt)
  print(__name__,'  :local_kwd:  ',local_kwd)
  
  if commit_password != local_kwd:
    return -1
  
  return 1

def generate_response(email,id):
  params={'id':id,'email':email}
  response=StateConstants.success() 
  
  token=token_service.create_token(params)
  token_dict={'token':token}
  
  response.update(token_dict)
  print(__name__,'  :generate_response:  ',response)
  return response