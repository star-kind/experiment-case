from flask import request
import sys
sys.path.append('./backstage/produce')
sys.path.append('./backstage/consts')
sys.path.append('./backstage/logger')
sys.path.append('./config')

import logining
import register
import modified_email
import modified_password
from state_consts import StateConstants
from app_factory import create_app
import records

app=create_app()

@app.route("/")#通过python装饰器的方法定义路由地址
def root():
  request_record()
  return logining.index_page() #用jinjia2引擎渲染页面并返回1个index.html页面

@app.route('/login', methods=['GET', 'POST'])
def handle_login():
  if request.method == 'POST':
    return logining.handle_login_data(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()   

@app.route('/register')
def register_page():
  return register.get_register_page()
  
@app.route('/register_account', methods=['GET', 'POST'])
def handle_register():
  if request.method == 'POST':
    return register.handle_register_data(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()   
  
@app.route('/modify-email')  
def modify_email():  
  return modified_email.modified_page(request)

@app.route('/handle-modify-email', methods=['GET', 'POST'])
def handle_modify_email():
  if request.method == 'POST':
    return modified_email.handler_modified_email(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()  
  
@app.route('/modify-password')  
def modify_password():  
  return modified_password.modify_page()
 
@app.route('/handle-modify-password', methods=['GET', 'POST'])
def handle_modify_password():
  if request.method == 'POST':
    return modified_password.handler_modified_password(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()    
  
def request_record():
  app.logger.info(request.headers)
  app.logger.info(request.method)
  app.logger.info(request.user_agent)
  app.logger.info(request.base_url)
  app.logger.info(request.url)
  app.logger.info(request.remote_addr)
  app.logger.info(request.url_root)
  app.logger.info(request.path)
  records.type_msg(headers=request.headers,method=request.method,
                   referrer=request.referrer,user_agent=request.user_agent,
                   base_url=request.base_url,url=request.url,
                   remote_addr=request.remote_addr,url_root=request.url_root,
                   path=request.path)  
  
if __name__ == '__main__':
  # 允许127.0.0.1:port、内网:port、外网:port 访问flask接口
  app.run(host='0.0.0.0',port=8085,debug=True)#定义app在某个端口运行