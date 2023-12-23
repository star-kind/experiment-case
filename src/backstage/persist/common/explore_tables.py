import execute_sentence

from app_factory import create_app
app=create_app()

# 查看库中所有的数据表  
def explore_tables():  
  sql_query = """
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%' AND tbl_name LIKE
            """
  sql_query1 = sql_query+" '"+app.config['DB_FILE_PATH']+"%';"            
  
  rows=execute_sentence.execute_fetch_records(sql_query1)
  app.logger.info(__name__+'.explore_tables.rows: '+str(rows))
