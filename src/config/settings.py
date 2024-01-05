import os
from datetime import datetime


def get_format_date():
    # 获取当前日期
    today = datetime.today().date()
    # 格式化日期
    formatted_date = today.strftime("%Y-%m-%d")
    return formatted_date  # 输出类似：2023-12-06


def get_log_path():
    log_file = os.getcwd() + "/journals/FlaskHistories-"
    format_date = get_format_date()
    logger_path = log_file + str(format_date) + ".log"

    # 获取日志文件的目录部分
    logger_dir = os.path.dirname(logger_path)
    # 如果目录不存在，创建它
    if not os.path.exists(logger_dir):
        os.makedirs(logger_dir)

    return logger_path


def get_db_file_path():
    db_file_path = os.getcwd() + "/databases/engineering.db"
    # 获取目录部分
    db_folder = os.path.dirname(db_file_path)
    # 如果目录不存在，创建它
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    return db_file_path


# 注意: 配置的名称必须是全大写形式，小写的变量将不会被读取
class PublicConfig:
    # 基础配置类，可以被其他环境配置继承
    SECRET_KEY = "your-token-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要跟踪模型修改
    JWT_SECRET_KEY = "your-json-web-token-secret-key"
    EXPIRES_IN = 60 * 60 * 6  # 有效期:1小时乘以6
    DB_FILE_PATH = get_db_file_path()
    TEMPLATES_DIR = os.getcwd() + "/templates"  # html模板目录
    FILE_LOG_PATH = get_log_path()
    STATIC_URL_PREFIX = "/static"  # 定义用户在浏览器地址栏中访问静态文件时的URL前缀
    STATIC_STORED_FOLDER = "../static"  # 应用内部存放静态文件的实际目录位置


class DevelopmentConfig(PublicConfig):
    # 开发环境配置
    DEBUG = True  # 启用调试模式
    TESTING = False  # 禁用测试模式
    ENV = "development"  # 设置环境为开发环境
    SQLALCHEMY_ECHO = True  # 输出SQL语句到控制台


class TestingConfig(PublicConfig):
    # 测试环境配置
    DEBUG = True
    TESTING = True
    ENV = "testing"
    WTF_CSRF_ENABLED = False  # 在测试中禁用CSRF保护


class ProductionConfig(PublicConfig):
    # 生产环境配置
    DEBUG = False
    TESTING = False
    ENV = "production"
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
    config_name = os.getenv("FLASK_ENV", "development")
    return multiple_config[config_name]
