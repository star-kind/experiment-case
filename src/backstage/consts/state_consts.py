class StateConstants:
  @staticmethod  
  def success(): 
    response={'state':200,'message':'Successful'} 
    return response  
    
  @staticmethod  
  def doubt_method():  
    response={'state':422,'message':'Doubtful Method'} 
    return response
  
  @staticmethod  
  def pwd_inconsistent(): 
    response ={'state':423,'message':'The new password entered twice is different'}
    return response
  
  @staticmethod  
  def param_empty(): 
    response ={'state':424,'message':'Parameters can not was empty'}
    return response
  
  @staticmethod  
  def contains_spaces(): 
    response ={'state':424,'message':'Error: Your commit parameter contains spaces'}
    return response
  
  @staticmethod  
  def email_out_limit(): 
    response ={'state':425,'message':'Error: Email length is can not greater than 40'}
    return response
  
  @staticmethod  
  def password_out_limit(): 
    response ={'state':426,'message':'Error: password length can not greater than 16'}
    return response
  
  @staticmethod  
  def password_less_length(): 
    response ={'state':427,'message':'Error: password length can not less than 4'}
    return response
  
  @staticmethod  
  def invalid_email(): 
    response ={'state':428,'message':'Error: Invalid email address format'}
    return response
    
  @staticmethod  
  def illegal_char(): 
    response ={'state':429,'message':'Error: Your commit parameter contains invalid characters'}
    return response
    
  @staticmethod  
  def no_such_user(): 
    response ={'state':430,'message':'Error: No such account'}
    return response
  
  @staticmethod  
  def password_incorrect(): 
    response ={'state':431,'message':'Error: Login Password is incorrect'}
    return response
  
  @staticmethod  
  def already_registered(): 
    response ={'state':432,'message':'Error: This email has already been registered by someone'}
    return response
  
  @staticmethod  
  def login_expire(): 
    response ={'state':433,'message':'Error: Login status has expired, please login retry'}
    return response
  
  @staticmethod  
  def consistent_email(): 
    response ={'state':434,'message':'Error: The replaced email is consistent with the original email'}
    return response
  
  @staticmethod  
  def pwd_contain_space(): 
    response ={'state':435,'message':'Error: Passwords contains a space'}
    return response
  
  @staticmethod  
  def user_status_amiss(): 
    response ={'state':436,'message':'Error: Your login status was amiss, please login retry'}
    return response
  
  @staticmethod  
  def origin_password_incorrect(): 
    response ={'state':431,'message':'Error: Original password is incorrect'}
    return response