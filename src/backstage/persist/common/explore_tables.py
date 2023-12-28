import execute_sentence


# 查看库中所有的数据表
def explore_tables():
    sql_query1 = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    rows = execute_sentence.execute_fetch_records(sql_query1, ())
    print(__name__ + ".explore_tables.rows: ", rows)


# explore_tables()
