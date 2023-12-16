import sys
sys.path.append('./backstage/logger')
sys.path.append('./backstage/consts')

from flask import render_template

import records
from state_consts import StateConstants
import token_service
import crud
import cryptography

def modify_page():
  html_path="ModifyPassWord.html"
  return render_template(html_path)

def handler_modified_password(req):
  records.type_msg('handler_modified_PassWord.Form: '+str(req.form))
  
  repeat_new_password=req.form['repeat_new_password']
  new_password=req.form['new_password']
  previous_password=req.form['previous_password']
  
  return kwd_handler(previous_password,new_password,repeat_new_password,req)

def kwd_handler(previous_password,new_password,repeat_new_password,req):
  result_dict=check_passwords(previous_password,new_password,repeat_new_password)
  if result_dict.get('flag',True) == False:
    return result_dict
  
  data_dict=check_token_data(req)
  if data_dict.get('flag','TrueDefault') == False:
    return data_dict
  
  user_email=data_dict.get('email','TrueDefault')
  key_dict=contrast_prev_pwd(user_email,previous_password)
  
  if key_dict.get('flag','TrueDefault') == False:
    return key_dict
  
  private_salt=key_dict.get('salt','TrueDefault')
  revamp_password(new_password,private_salt,user_email)  
  return StateConstants.success()
  
def check_passwords(previous_password,new_password,repeat_new_password):
  result_dict={}
  # 检查密码是否含有空格
  for s in [previous_password, new_password, repeat_new_password]:
    if ' ' in s:
        result_dict=StateConstants.pwd_contain_space()|{'flag':False}
        break

  # 检查密码长度是否大于限制
  for s in [previous_password, new_password, repeat_new_password]:
    if len(s) > 16:
        result_dict=StateConstants.password_out_limit()|{'flag':False}
        break

  # 检查字符串长度是否小于4
  for s in [previous_password, new_password, repeat_new_password]:
    if len(s) < 4:
        result_dict=StateConstants.password_less_length()|{'flag':False}
        break

  # 检查两次新密码是否不一致
  if new_password != repeat_new_password:
    result_dict=StateConstants.pwd_inconsistent()|{'flag':False}
    
  # 检查参数是否为空
  for s in [previous_password,new_password,repeat_new_password]:
    if not s:
        result_dict=StateConstants.param_empty()|{'flag':False}
        break    
  return result_dict
  
def check_token_data(request):
  res_dict={}
  token_str=token_service.get_token_from_req(request)
  resp=token_service.verify_get_usr_data(token_str)
  
  flag=resp.get('flag','defaultValue')
  if flag == False :
    res_dict = StateConstants.login_expire() | {'flag':False}
    
  else:
    user_email=resp.get('email','defaultEmail')
    user_id=resp.get('id','defaultID')
    records.type_msg('user_email: '+str(user_email)+'\n'+'user_id: '+str(user_id))  

    res_dict={'email':user_email,'id':user_id,'flag':True} 
  return res_dict    

def contrast_prev_pwd(user_email,commit_old_pwd):
  res_dict={}
  usr_list=crud.select_one_by_email(user_email)
  
  if len(usr_list) == 0:
    res_dict=StateConstants.user_status_amiss() | {'flag':False}
  records.type_msg('verify_prev_pwd.usr_list: '+str(usr_list))
  
  prev_pwd_txt=usr_list[0][2]
  salt_key=usr_list[0][3]
  
  prev_password=cryptography.aes_decrypt(salt_key,prev_pwd_txt)
  records.type_msg('verify_prev_pwd.prev_password: '+str(prev_password))
  
  if prev_password != commit_old_pwd:
    res_dict=StateConstants.origin_password_incorrect() | {'flag':False}
  
  if res_dict.get('flag',True) != False:
    res_dict2={'salt':salt_key}
    return res_dict2
  else:
    return res_dict

def revamp_password(new_password,salt_key,user_email):
  new_password_text=cryptography.aes_encrypt(salt_key,new_password)
  records.type_msg('revamp_password.new_password_text: '+str(new_password_text))
  
  crud.update_password_by_email(new_password_text,user_email)
  