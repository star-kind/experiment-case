import re
import records
from state_consts import StateConstants
import public_platform
import account_crud
import cryptography
import check_params as ck

unqualified_flag = {"flag": False}


def alter_pwd_service(previous_password, new_password, repeat_new_password, user_email):
    result_dict = check_params(
        previous_password, new_password, repeat_new_password, user_email
    )
    if result_dict.get("flag", True) == False:
        return result_dict

    key_dict = contrast_prev_pwd(user_email, previous_password)

    if key_dict.get("flag", "TrueDefault") == False:
        return key_dict

    private_salt = key_dict.get("salt", "TrueDefault")
    revamp_password(new_password, private_salt, user_email)
    return StateConstants.success()


def check_params(previous_password, new_password, repeat_new_password, user_mail):
    params_valid = ck.check_params(
        previous_password, new_password, repeat_new_password, user_mail
    )
    if params_valid == False:
        return StateConstants.param_empty()

    # 检查密码是否含有空格
    for s in [previous_password, new_password, repeat_new_password, user_mail]:
        if " " in s:
            state = StateConstants.pwd_contain_space()
            return {**state, **unqualified_flag}

    # 检查密码长度是否大于限制
    for s in [previous_password, new_password, repeat_new_password]:
        if len(s) > public_platform.pwd_len_upper_limit:
            state = StateConstants.password_out_limit()
            return {**state, **unqualified_flag}

    # 检查字符串长度是否小于4
    for s in [previous_password, new_password, repeat_new_password]:
        if len(s) < public_platform.pwd_len_lower_limit:
            state = StateConstants.password_less_length()
            return {**state, **unqualified_flag}

    # 检查两次新密码是否不一致
    if new_password != repeat_new_password:
        state = StateConstants.pwd_inconsistent()
        return {**state, **unqualified_flag}

    # 检查邮箱正则
    if not re.match(public_platform.mail_regex_rule, str(user_mail)):
        state = StateConstants.invalid_email()
        return {**state, **unqualified_flag}

    # 检查参数是否为空
    for s in [previous_password, new_password, repeat_new_password]:
        if not s:
            state = StateConstants.param_empty()
            return {**state, **unqualified_flag}

    qualified_flag = {"flag": True}
    return qualified_flag


def contrast_prev_pwd(user_email, commit_old_pwd):
    user_tuple = account_crud.select_user_by_email(user_email)

    if user_tuple == None:
        state = StateConstants.user_status_amiss()
        return {**state, **unqualified_flag}
    records.type_msg(verify_prev_pwd_user_tuple=user_tuple)

    prev_pwd_txt = user_tuple[2]
    salt_key = user_tuple[3]

    prev_password = cryptography.aes_decrypt(salt_key, prev_pwd_txt)
    records.type_msg(verify_prev_pwd_prev_password=prev_password)

    if prev_password != commit_old_pwd:
        state = StateConstants.origin_password_incorrect()
        return {**state, **unqualified_flag}

    salt_flag = {"salt": salt_key, "flag": True}
    return salt_flag


def revamp_password(new_password, salt_key, user_email):
    new_password_text = cryptography.aes_encrypt(salt_key, new_password)
    records.type_msg(revamp_password_new_password_text=new_password_text)
    account_crud.update_password_by_email(new_password_text, user_email)


# prev_kwd = "9999999"
# new_kwd = "999999900"
# repeat_new_kwd = "999999900"
# usr_mail = "title@yon.com"
# result = alter_pwd_service(prev_kwd, new_kwd, repeat_new_kwd, usr_mail)
# print(result)
