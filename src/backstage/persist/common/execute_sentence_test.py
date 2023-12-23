import connected
  
# 仅执行，无返回
def execute_no_result(sql_sentence:str)->None:
  con = connected.connect_database()
  print(str(__name__)+'.class.execute_no_res-sql_sentence: '+str(sql_sentence))
  
  cur = con.cursor()
  cur.execute(str(sql_sentence))
  con.commit()
  con.close()

# 执行，且返回1个列表
def execute_fetch_records(sql_sentence:str)->list:
  con = connected.connect_database()
  print(str(__name__)+'.class.execute_fetch_records-sql_sentence: '+str(sql_sentence))
  
  cur = con.cursor()
  cur.execute(str(sql_sentence))
  
  results = cur.fetchall() # 获取查询结果
  print(str(__name__)+'.class.execute_fetch_records-results: '+str(results))
  
  con.commit()
  con.close()
  return results  