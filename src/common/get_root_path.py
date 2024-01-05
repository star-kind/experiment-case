import os


def find_file_directory_recursively(filename, current_path=os.getcwd()):
    # 检查当前目录下是否存在该文件
    file_path = os.path.join(current_path, filename)
    if os.path.exists(file_path):
        execute_file_path = os.path.abspath(os.path.dirname(file_path))
        print("execute_file_path ", execute_file_path)
        return execute_file_path

    # 获取当前目录的父目录路径
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))

    # 如果当前目录不是根目录（"/"或"C:\"等），则向上一级目录递归查找
    if current_path != parent_path:
        return find_file_directory_recursively(filename, parent_path)

    # 如果已搜索到根目录仍找不到文件，则返回None表示未找到
    return None


# target_file = "hinge.py"
# directory_path = find_file_directory_recursively(target_file)
# if directory_path is not None:
#     print(f'找到文件 "{target_file}" 所在的目录: {directory_path}')
# else:
#     print(f"未能在任何目录下找到文件: {target_file}")
