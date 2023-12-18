from app_factory import create_app
app=create_app()
  
def type_history(requests):
  sentence = 'headers: ' + str(requests.headers) + '  '
  sentence += 'form: ' + str(requests.form) + '  '
  sentence += 'args: ' + str(requests.args) + '  '
  sentence += 'data: ' + str(requests.data) + '  '
  sentence += 'method: ' + str(requests.method) + '  '
  sentence += 'referrer: ' + str(requests.referrer) + '  '
  sentence += 'user_agent: ' + str(requests.user_agent) + '  '
  sentence += 'url: ' + str(requests.url) + '  '
  sentence += 'base_url: ' + str(requests.base_url) + '  '
  sentence += 'url_root: ' + str(requests.url_root) + '  '
  sentence += 'path: ' + str(requests.path) + '  '
  sentence += 'script_root: ' + str(requests.script_root) + '  '
  sentence += 'remote_addr: ' + str(requests.remote_addr) + '  '
  sentence += 'get_json: ' + str(requests.get_json()) + '  '
  sentence += '\n'
  app.logger.info(sentence)
  
def type_msg(msg):
  app.logger.info(str(msg))  