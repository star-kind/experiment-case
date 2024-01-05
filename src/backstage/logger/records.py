import os
import settings
import public_platform as pub


def get_text_file():
    text_file = pub.journal_previous_path
    text_file += settings.get_format_date()
    text_file += ".log"

    # 判断文件是否存在
    if os.path.exists(text_file):
        print("Type Message: File already exists")
    else:
        # 创建文件
        with open(text_file, "w") as f:
            print("Type Message: File being created success")
    return text_file


def type_msg(**msg):
    print(msg)
    string_msg = str(msg)
    text_file = get_text_file()

    with open(text_file, mode="a") as file:
        file.write(string_msg)
        file.write("\n")  # 换行
