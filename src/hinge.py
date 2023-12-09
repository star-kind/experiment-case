import sys
sys.path.append('./backstage/produce')
sys.path.append('./backstage/consts')
sys.path.append('./config')

from flask import request
from flask_cors import CORS

import logining
import register
import modified_email
import modified_password
from state_consts import StateConstants
from app_factory import create_app

app=create_app()

# 设置CORS（跨域资源共享）头
CORS(app)

# 设置静态文件路径
app.template_folder = app.config['TEMPLATES_DIR']
app.static_url_path=app.config['STATIC_URL_PREFIX']
app.static_folder=app.config['STATIC_STORED_FOLDER']

@app.route("/")#通过python装饰器的方法定义路由地址
def root():
  app.logger.info(request.headers)
  app.logger.info(request.method)
  return logining.index_page() #用jinjia2引擎渲染页面并返回1个index.html页面

@app.route('/login', methods=['GET', 'POST'])
def handle_login():
  if request.method == 'POST':
    return logining.handle_login_data(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()   

@app.route('/register')
def register_page():
  app.logger.info(request.headers)
  app.logger.info(request.method)
  return register.get_register_page()
  
@app.route('/register_account', methods=['GET', 'POST'])
def handle_register():
  if request.method == 'POST':
    return register.handle_register_data(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()   
  
@app.route('/modify-email')  
def modify_email():  
  app.logger.info('modify-email.request.headers: '+str(request.headers))
  return modified_email.modified_page(request)

@app.route('/handle-modify-email', methods=['GET', 'POST'])
def handle_modify_email():
  if request.method == 'POST':
    return modified_email.handler_modified_email(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()  
  
@app.route('/modify-password')  
def modify_password():  
  app.logger.info('modify-PassWord.request.headers: '+str(request.headers))
  return modified_password.modify_page()
 
@app.route('/handle-modify-password', methods=['GET', 'POST'])
def handle_modify_password():
  if request.method == 'POST':
    return modified_password.handler_modified_password(request)
  elif request.method == 'GET':
    return StateConstants.doubt_method()    
  
if __name__ == '__main__':
  app.run(port=8085,debug=True)#定义app在某个端口运行