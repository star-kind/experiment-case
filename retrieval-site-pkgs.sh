# 在Linux中，可以通过以下命令查找当前Python版本的site-packages目录：
python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
