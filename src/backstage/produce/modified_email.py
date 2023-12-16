import sys
sys.path.append('./backstage/logger')
sys.path.append('./backstage/consts')

import re
from flask import render_template
import records
from state_consts import StateConstants
import token_service
import cryptography

sys.path.append('./backstage/persist')
import crud

def modified_page(request):
  html_path="ModifyEmail.html"
  print('modified_page.request.headers: ',request.headers)
  return render_template(html_path)

def handler_modified_email(request):
  records.type_msg('handler_modified_email.form: '+str(request.form))
  new_email=request.form['new_email']
  password=request.form['password']
  
  token_str=token_service.get_token_from_req(request)
  resp=token_service.verify_get_usr_data(token_str)
  
  flag=resp.get('flag','default_value')
  if flag == False :
    return StateConstants.login_expire()  
  
  origin_email=resp.get('email','defaultEmail')
  records.type_msg('Origin_email: '+str(origin_email))
  
  return previous_check(new_email,password,origin_email)
  
def previous_check(new_email,password,origin_email):
  if not re.match(r"[^@]+@[^@]+\.[^@]+", str(new_email)):
      return StateConstants.invalid_email()
  
  if any(' ' in str(s) for s in [new_email, password]):
      return StateConstants.contains_spaces()
    
  if len(str(password)) < 4:
      return StateConstants.password_less_length()    
    
  return contrast_email(new_email,password,origin_email)  
  
def contrast_email(new_email,commit_password,origin_email):
    rows=crud.select_one_by_email(origin_email)#TODO
    
    if len(rows) < 1 :
      return StateConstants.login_expire()
    records.type_msg('Contrast_email.Rows: '+str(rows))
    
    previous_email=rows[0][1]
    if previous_email == new_email:
      return StateConstants.consistent_email()
    
    contrast_pwd=contrast_password(rows,commit_password)
    if contrast_pwd == False:
      return StateConstants.password_incorrect()

    return revamp_email(rows,new_email)
  
def contrast_password(rows,commit_password):  
  db_pwd_txt=rows[0][2]
  db_salt=rows[0][3]
  pwd=cryptography.aes_decrypt(db_salt,db_pwd_txt)
  records.type_msg('contrast_password.database.password: '+str(pwd))
  
  if pwd != commit_password:
    return False
  return True
  
def revamp_email(rows,new_email):
  uid=rows[0][0]
  crud.update_email_by_id(new_email,uid)
  
  user_data={'email':new_email,'id':uid}
  new_token=token_service.create_token(user_data)
   
  # 创建新的字典，合并 dict1 和 dict2 的内容 
  response=StateConstants.success()|{'token':new_token}
  records.type_msg(response)
  
  return response