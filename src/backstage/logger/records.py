import os
import settings 

def get_text_file():
  text_file="./journals/TypeMessage-"
  text_file+=settings.get_format_date()
  text_file+=".log"
  
  # 判断文件是否存在
  if os.path.exists(text_file):
    print("Type Message 文件已存在")
  else:
    # 创建文件
    with open(text_file, 'w') as f:
        print("Type Message 文件创建成功")
  return text_file

def type_msg(**msg):
  print(msg)
  string_msg=str(msg)
  text_file=get_text_file()
  
  with open(text_file, mode='a') as file:
    file.write(string_msg)
    file.write('\n') # 换行
