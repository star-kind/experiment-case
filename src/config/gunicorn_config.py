import multiprocessing
import logging
import sys
sys.path.append('./config')
from settings import get_format_date

current_time = get_format_date()

# 配置Gunicorn启动后的进程名称，方便top、ps等指令的辨别
proc_name = "experiment-case"

# 监听IP放宽，以便于Docker之间、Docker和宿主机之间的通信
bind = "0.0.0.0:8085"

# 定义同时开启的处理请求的进程数量，根据网站流量适当调整
workers = multiprocessing.cpu_count() 

# 采用gevent库，支持异步处理请求，提高吞吐量
worker_class = "gevent"

# # 设置每个工作进程的最大并发连接数
worker_connections = 1000

# # 设置工作进程在接收完请求后最大等待时间（秒），超时后会重启该工作进程
timeout = 30

# # 设置启动多少个备用工作进程，在主进程检测到工作进程异常退出后自动启动
keepalive = 2

# # 设置在工作进程重启前，可以处理的最大请求数量
max_requests = 1000

# # 设置在工作进程重启前，处理请求的最大总时间（秒）
max_requests_jitter = 50

# # 设置工作进程在空闲多久后自动重启（秒）
worker_idle_timeout = 60

# # 设置工作进程在退出前，是否先等待当前请求处理完成
graceful_timeout = 30

# 设置错误日志文件路径和级别
errorlog = "./journals/gunicorn-error-" + str(current_time) + ".log"
loglevel = "info"

# 设置访问日志文件路径
accesslog = "./journals/gunicorn-access-" + str(current_time) + ".log"

# 创建一个logger实例
logger = logging.getLogger("gunicorn.error")
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
file_handler = logging.FileHandler(errorlog)
file_handler.setLevel(logging.INFO)

# 创建一个handler，用于输出到控制台
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

# 设置formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def post_fork(server, worker):
    # 在工作进程启动后，将标准输出和标准错误重定向到父进程的相应文件描述符
    worker.stdout = sys.stdout
    worker.stderr = sys.stderr