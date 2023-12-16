from flask import Flask
from flask_cors import CORS
import logging
from settings import get_config

def create_app():
    # 创建Flask对象并初始化
    app = Flask(__name__)
    
    # 设置CORS（跨域资源共享）头
    CORS(app)

    # 加载配置
    config_class = get_config()
    app.config.from_object(config_class)
    
    app = set_logger(app)
    app = get_conf_app(app)
    return app

def set_logger(app):
  # 创建一个 FileHandler 对象，并将其添加到 logger 中
  file_handler = logging.FileHandler(app.config['FILE_LOG_PATH'])
  # 设置日志格式
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)

  app.logger.addHandler(file_handler)
  return app

def get_conf_app(app):
  # 设置静态文件路径
  app.template_folder = app.config['TEMPLATES_DIR']
  app.static_url_path=app.config['STATIC_URL_PREFIX']
  app.static_folder=app.config['STATIC_STORED_FOLDER']
  return app