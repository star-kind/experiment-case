import re
import essay_crud
from state_consts import StateConstants
import public_platform
import account_crud
import cont_cipher
import check_params as chk


def write_blog_service(title: str, content: str, mail: str, uid: int, encrypt_key: str):
    if type(uid) != int:
        return StateConstants.parameter_invaild_type()

    clean_content = str(content).replace(" ", "")
    clean_title = str(title).replace(" ", "")
    if chk.check_params(clean_title, clean_content, mail, uid, encrypt_key) == False:
        return StateConstants.param_empty()

    if len(str(mail)) > public_platform.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(public_platform.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    result_check = user_check(mail)
    if result_check.get("flag", "Default") == False:
        return StateConstants.no_such_user()

    user_tuple = result_check.get("user", "DefaultString")

    # if user_id != uid
    if user_tuple[0] != uid:
        return StateConstants.user_status_amiss()

    clean_encrypt_key = str(encrypt_key).replace(" ", "")
    if encrypt_key != None or clean_encrypt_key != "":
        if " " in str(encrypt_key).strip():
            return StateConstants.contains_spaces()
        content = cont_cipher.encrypt(clean_encrypt_key, str(content).strip())

    essay_crud.inserts_essay(
        str(title).strip(), str(content).strip(), uid, mail, clean_encrypt_key.strip()
    )
    return StateConstants.success()


def user_check(email):
    user_row = account_crud.select_user_by_email(email)
    print("user_row", user_row)

    if user_row == None:
        # 检查是否有此账户
        return {"flag": False, "user": None}
    else:
        return {"flag": True, "user": user_row}


# title = 7755.009
# content = 1333.5000888
# uid = 6
# mail = "testUser@yon.com"
# encrypt_str = 777
# result = write_blog_service(title, content, mail, uid, encrypt_str)
# print("result", result)
