import connected


# 仅执行,无返回
def execute_no_result(sql_sentence: str, param_tuple: ()) -> None:
    print("execute_no_res-sql_sentence: ", sql_sentence)
    con = connected.connect_database()
    cur = con.cursor()

    if param_tuple == ():
        cur.execute(str(sql_sentence))
    else:
        cur.execute(str(sql_sentence), param_tuple)

    con.commit()
    cur.close()
    con.close()


# 执行,且返回1个列表
def execute_fetch_records(sql_sentence: str, param_tuple: ()) -> list:
    print("execute_fetch_records-sql_sentence: ", sql_sentence)
    con = connected.connect_database()
    cur = con.cursor()

    if param_tuple == ():
        cur.execute(str(sql_sentence))
    else:
        cur.execute(str(sql_sentence), param_tuple)

    results = cur.fetchall()  # 获取查询结果
    # print("execute_fetch_records-results: ", results)

    con.commit()

    cur.close()
    con.close()
    return results


# 执行,且返回1行记录
def execute_fetch_one_row(sql_sentence: str, param_tuple: ()) -> list:
    print("execute_fetch_records-sql_sentence: ", sql_sentence)
    con = connected.connect_database()
    cur = con.cursor()

    if param_tuple == ():
        cur.execute(str(sql_sentence))
    else:
        cur.execute(str(sql_sentence), param_tuple)

    results = cur.fetchone()  # 获取查询结果
    print("execute_fetch_records-results: ", results)

    con.commit()

    cur.close()
    con.close()
    return results
