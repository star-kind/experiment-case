import connected


def get_table_structure(table_name):
    # 连接到SQLite数据库
    con = connected.connect_database()
    c = con.cursor()

    # 查询表的结构
    c.execute(f"PRAGMA table_info({table_name})")
    table_structure = c.fetchall()

    # 获取列名和数据类型
    columns = []
    for row in table_structure:
        column_name = row[1]
        data_type = row[2]
        columns.append((column_name, data_type))

    # 关闭连接
    con.close()

    return columns


# table_name = "essay"
# table_structure = get_table_structure(table_name)

# for column in table_structure:
#     print(f"Column: {column[0]}, Type: {column[1]}")
