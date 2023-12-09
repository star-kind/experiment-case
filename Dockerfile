# 使用官方的Python 3.12镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将项目所需的依赖文件复制到工作目录
COPY requirements.txt .

# 安装项目所需的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将项目源代码复制到工作目录
COPY src .

COPY ali-cloud-mirror.list .
COPY apt-execute.sh .

# 暴露端口号为8085
EXPOSE 8085

CMD ["bash", "gunicorn-start.sh"]