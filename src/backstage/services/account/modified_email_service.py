import re
from flask import render_template
import records
from state_consts import StateConstants
import token_service
import cryptography
import account_crud
import public_platform
import check_params


def modified_email_service(new_email, password, origin_email):
    params_valid = check_params.check_params(new_email, password, origin_email)
    if params_valid == False:
        return StateConstants.param_empty()

    if not re.match(public_platform.mail_regex_rule, str(new_email)):
        return StateConstants.invalid_email()

    if any(" " in str(s) for s in [new_email, password]):
        return StateConstants.contains_spaces()

    if len(str(password)) < public_platform.pwd_len_lower_limit:
        return StateConstants.password_less_length()

    return contrast_email(new_email, password, origin_email)


def contrast_email(new_email, commit_password, origin_email):
    rows = account_crud.select_user_by_email(origin_email)

    if rows == None:
        return StateConstants.login_expire()
    records.type_msg(Contrast_email_Rows=rows)

    previous_email = rows[1]
    if previous_email == new_email:
        return StateConstants.consistent_email()

    contrast_pwd = contrast_password(rows, commit_password)
    if contrast_pwd == False:
        return StateConstants.password_incorrect()

    return revamp_email(rows, new_email)


def contrast_password(rows, commit_password):
    db_pwd_txt = rows[2]
    db_salt = rows[3]
    pwd = cryptography.aes_decrypt(db_salt, db_pwd_txt)
    records.type_msg(contrast_password_database_password=pwd)

    if pwd != commit_password:
        return False
    return True


def revamp_email(rows, new_email):
    uid = rows[0]
    account_crud.update_email_by_id(new_email, uid)

    user_data = {"email": new_email, "id": uid}
    new_token = token_service.create_token(user_data)

    # 创建新的字典，合并 dict1 和 dict2 的内容
    resp = {"token": new_token}
    state = StateConstants.success()

    response = {**state, **resp}
    records.type_msg(revamp_email_response=response)
    return response


# result = modified_email_service("newaccount@ubm.com", "9999999", "title@yon.com")
# print("modified_email_service result", result)
