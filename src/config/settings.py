import os
from datetime import datetime

def get_format_date():
    # 获取当前日期
    today = datetime.today().date()
    # 格式化日期
    formatted_date = today.strftime('%Y-%m-%d')
    # print(formatted_date)  # 输出类似：2023-12-06
    return formatted_date

def get_log_path():
    log_file=os.getcwd()+'/journals/FlaskHistories-'
    format_date=get_format_date()
    logger_path=log_file+str(format_date)+'.log'
    return logger_path

# 注意: 配置的名称必须是全大写形式，小写的变量将不会被读取
class PublicConfig:
    # 基础配置类，可以被其他环境配置继承
    SECRET_KEY = 'your-token-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要跟踪模型修改
    JWT_SECRET_KEY = 'your-json-web-token-secret-key'
    EXPIRES_IN = 60 * 60  # 1小时有效期
    DB_FILE_PATH= os.getcwd()+'/databases/engineering.db'
    TEMPLATES_DIR= os.getcwd()+ '/templates' # html模板目录
    FILE_LOG_PATH= get_log_path()
    STATIC_URL_PREFIX= '/static' #定义用户在浏览器地址栏中访问静态文件时的URL前缀
    STATIC_STORED_FOLDER='../static' #应用内部存放静态文件的实际目录位置
 
class DevelopmentConfig(PublicConfig):
    # 开发环境配置
    DEBUG = True  # 启用调试模式
    TESTING = False  # 禁用测试模式
    ENV = 'development'  # 设置环境为开发环境
    SQLALCHEMY_ECHO = True  # 输出SQL语句到控制台

class TestingConfig(PublicConfig):
    # 测试环境配置
    DEBUG = True
    TESTING = True
    ENV = 'testing'
    WTF_CSRF_ENABLED = False  # 在测试中禁用CSRF保护

class ProductionConfig(PublicConfig):
    # 生产环境配置
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SQLALCHEMY_ECHO = False

# 根据环境变量 FLASK_ENV 来选择配置
# FLASK_ENV 环境变量需要自己手动配置: export FLASK_ENV=xxx
multiple_config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)

def get_config():
    # 若无环境变量FLASK_ENV，就启用development配置类
    config_name = os.getenv('FLASK_ENV', 'development')
    return multiple_config[config_name]