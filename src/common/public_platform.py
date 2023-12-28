# 数据库路径
DATABASE_PATH = "/path/experiment-case/src/databases/Application.db"

mail_len_upper_limit = 128  # 邮箱名称长度上限
pwd_len_upper_limit = 16  # 密码名称长度上限

mail_len_lower_limit = 4  # 邮箱名称长度下限
pwd_len_lower_limit = 4  # 密码名称长度上限

mail_regex_rule = r"[^@]+@[^@]+\.[^@]+"  # 邮箱地址正则

expire_key_name = "expires"  # 令牌中的过期时间

plaintext_rating = 0  # 文章未加密之级别

encrypted_rating = 1  # 文章业已加密之级别

rows_per_page = 5  # 文章分页每页行数

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
