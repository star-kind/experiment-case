from flask import Flask
import logging
from settings import get_config

def create_app():
    # 创建Flask对象并初始化
    app = Flask(__name__)

    # 加载配置
    config_class = get_config()
    app.config.from_object(config_class)
    
    app2 = set_logger(app)
    return app2

def set_logger(app):
  # 创建一个 FileHandler 对象，并将其添加到 logger 中
  file_handler = logging.FileHandler(app.config['FILE_LOG_PATH'])
  # 设置日志格式
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)

  app.logger.addHandler(file_handler)
  return app