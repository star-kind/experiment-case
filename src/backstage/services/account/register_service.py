import re

from state_consts import StateConstants
import cryptography
import account_crud
import public_platform
import check_params


def register_deals_service(email, password, re_password):
    if str(password) != str(re_password):
        return StateConstants.pwd_inconsistent()

    params_valid = check_params.check_params(email, password, re_password)
    if params_valid == False:
        return StateConstants.param_empty()

    if any(" " in str(s) for s in [email, re_password, password]):
        return StateConstants.contains_spaces()

    if len(str(email)) > public_platform.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if len(str(password)) > public_platform.pwd_len_upper_limit:
        return StateConstants.password_out_limit()

    if len(str(password)) < public_platform.pwd_len_lower_limit:
        return StateConstants.password_less_length()

    if not re.match(public_platform.mail_regex_rule, str(email)):
        return StateConstants.invalid_email()

    if any(c in str(email) for c in public_platform.illegal_chars):
        return StateConstants.illegal_char()

    if check_repeat_user(email) > 0:
        return StateConstants.already_registered()

    stored_usr(email, password)
    return StateConstants.success()


def check_repeat_user(email):
    user_list = account_crud.select_user_by_email(email)

    if user_list is not None:
        print("user_list", user_list)
        return len(user_list)
    else:
        print("Indicates that the account name has not been preempted")
        return 0


def stored_usr(email, password):
    # 获取salt
    salt_str = cryptography.get_salt()
    # 获取密文
    cipher_txt = cryptography.aes_encrypt(salt_str, password)
    account_crud.inserts(email, cipher_txt, salt_str)


# result = register_deals_service("missWV@yon.com", "9999999", "9999999")
# print("register result", result)
