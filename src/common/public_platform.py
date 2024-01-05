import get_root_path

# 根文件
root_execute_file = "hinge.py"

# 根文件所处目录
root_execute_dir = get_root_path.find_file_directory_recursively(root_execute_file)

# 数据库路径
DATABASE_PATH = root_execute_dir + "/databases/Application.db"

# 日志文本文件名称前缀
journal_previous_path = root_execute_dir + "/journals/TypeMessage-"

mail_len_upper_limit = 128  # 邮箱名称长度上限
pwd_len_upper_limit = 16  # 密码名称长度上限

mail_len_lower_limit = 4  # 邮箱名称长度下限
pwd_len_lower_limit = 4  # 密码名称长度上限

mail_regex_rule = r"[^@]+@[^@]+\.[^@]+"  # 邮箱地址正则

chinese_regex = r"[\u4e00-\u9fa5]"  # 中文正则

expire_key_name = "expires"  # 令牌中的过期时间

plaintext_rating = 0  # 文章未加密之级别

encrypted_rating = 1  # 文章业已加密之级别

rows_per_page = 5  # 文章分页每页行数

article_encrypt_upper = 32  # 文章密钥长度上限

# 非法字符集
illegal_chars = [
    "“",
    "‘",
    "'",
    '"',
    "~",
    "!",
    "#",
    "$",
    "%",
    "^",
    "&",
    "(",
    ")",
    "*",
    "+",
    "=",
    "[",
    "]",
    ";",
    ":",
    "\\",
    "/",
    "<",
    ">",
    ",",
    "，",
    "。",
]
