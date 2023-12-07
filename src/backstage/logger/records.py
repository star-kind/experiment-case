from app_factory import create_app
app=create_app()
  
def type_history(histories):
  separator="\n"
  string_list:list=['headers:',str(histories.headers),'form:',str(histories.form),'args:',str(histories.args),'data:',str(histories.data)]
  sentence=separator.join(string_list)
  
  app.logger.info(sentence)
  
def type_msg(msg):
  app.logger.info(str(msg))  