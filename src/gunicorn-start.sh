# 设置环境变量
export FLASK_APP=hinge.py
export FLASK_ENV=development
export GUNICORN_CMD_ARGS="--worker-class gevent --workers 4"

# 启动gunicorn
gunicorn -c config/gunicorn_config.py hinge:app