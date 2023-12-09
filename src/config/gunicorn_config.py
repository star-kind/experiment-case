# gunicorn_config.py
import multiprocessing

# 配置Gunicorn启动后的进程名称，方便top、ps等指令的辨别
proc_name = "experiment-case"

# 监听IP放宽，以便于Docker之间、Docker和宿主机之间的通信
bind = "0.0.0.0:8085"

# 定义同时开启的处理请求的进程数量，根据网站流量适当调整
workers = multiprocessing.cpu_count() * 2 + 1

# 采用gevent库，支持异步处理请求，提高吞吐量
worker_class = "gevent"

timeout = 30
