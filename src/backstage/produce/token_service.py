import datetime
import jwt

import sys
sys.path.append('./backstage/consts')
from state_consts import StateConstants
from app_factory import create_app

app=create_app()
expire_key_name='exp' # 过期时间的键名

def create_token(param_body:dict):
  param_body[expire_key_name]=int(datetime.datetime.now().timestamp())+app.config['EXPIRES_IN']
  app.logger.info(str(__name__)+'.create_token.param_body: '+str(param_body))
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
  token = None
  try:
    # 使用配置文件中的值
    token = jwt.encode(payload=param_body, key=app.config['SECRET_KEY'], algorithm='HS256')
  except Exception as e:
    app.logger.error("获取token失败:{}".format(e))
    
  app.logger.info(str(__name__)+'.create_token.token: '+str(token))  
  return token
  

def verify_token(token):
    try:
        # 使用SECRET_KEY从配置文件中解码令牌
      decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
      app.logger.info(str(__name__)+'.verify_token__decoded_token: ',decoded_token)  
        
      # 假设 decoded_token[expire_key_name] 是一个 Unix 时间戳
      expire_time = datetime.datetime.fromtimestamp(decoded_token[expire_key_name])
      
      # 检查令牌是否过期
      if datetime.datetime.now() > expire_time:
          return False
      return True
    
    except jwt.ExpiredSignatureError:
      app.logger.error("Token已过期")
      return False

    except jwt.InvalidTokenError as e:
      app.logger.error("无效的Token: {}".format(e))
      return False  
    
def get_data_by_token(token):
    decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])  
    app.logger.info(str(__name__)+'.get_data_by_token_decoded_token: '+str(decoded_token))
    return decoded_token
  
def get_token_from_req(request):
  author_str=request.headers.get('Authorization','Default')
  print('request.headers.Authorization:',author_str,'\n')
  
  token_str=author_str.replace("Bearer ", "")
  print('token_str:',token_str,'\n')  
  return token_str

def verify_get_usr_data(token_string):
  status=verify_token(token_string)
  
  if status == False:
    flag_dict={'flag':status}
    return flag_dict
  
  usr_info=get_data_by_token(token_string)
  app.logger.info('Verify_get_usr_data.usr_info: ',usr_info)
  return usr_info