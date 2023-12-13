import sys
sys.path.append('./backstage/logger')
sys.path.append('./backstage/consts')
sys.path.append('./backstage/persist')

from flask import render_template
import re

import records
from state_consts import StateConstants
import cryptography
import crud

def get_register_page():
  html_path="register.html"
  return render_template(html_path)

def handle_register_data(request_data):
  records.type_history(request_data)
  return reg_verify(request_data)
  
def reg_verify(request_data):
    email=request_data.form['email']
    password=request_data.form['password']
    re_password=request_data.form['repeat_password']
    illegal_chars=['“', '‘', "'", '"', '~', '!', '#', '$', '%', '^', '&', '(', ')', '*', '+', '=', '[', ']', ';', ':', '\\', '/', '<', '>', ',','，','。']
    
    if str(password) != str(re_password):
      return StateConstants.pwd_inconsistent()
      
    if len(dict(request_data.form)) == 0:
      return StateConstants.param_empty()
      
    if any(' ' in str(s) for s in [email, re_password, password]):
      return StateConstants.contains_spaces()
      
    if len(str(email)) > 40:
      return StateConstants.email_out_limit()
      
    if len(str(password)) > 16:
      return StateConstants.password_out_limit()
      
    if len(str(password)) < 4:
      return StateConstants.password_less_length()
      
    if not re.match(r"[^@]+@[^@]+\.[^@]+", str(email)):
      return StateConstants.invalid_email()
      
    if any(c in str(email) for c in illegal_chars):
      return StateConstants.illegal_char()
  
    if check_repeat_user(email) > 0:
      return StateConstants.already_registered()
    
    stored_usr(email,password)  
    return StateConstants.success()
  
def check_repeat_user(email):
  user_list=crud.select_one_by_email(email)
  
  if user_list is not None:
    print(__name__,'  :user_list= ',user_list)
    return len(user_list)
  else:
    # 返回0或其他适当的默认值/错误信息
    return 0
  
def stored_usr(email,password):
    # 获取salt
    salt_str = cryptography.get_salt()
    # 获取密文
    cipher_txt=cryptography.aes_encrypt(salt_str,password)
    
    crud.inserts(email,cipher_txt,salt_str)