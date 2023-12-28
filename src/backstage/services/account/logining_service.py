import re

from state_consts import StateConstants
import account_crud
import cryptography
import token_service
import public_platform
import check_params


def logining_deals_service(email, password):
    params_valid = check_params.check_params(email, password)
    if params_valid == False:
        return StateConstants.param_empty()

    elif any(" " in str(s) for s in [email, password]):
        return StateConstants.contains_spaces()

    elif len(str(email)) > public_platform.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    elif len(str(password)) > public_platform.pwd_len_upper_limit:
        return StateConstants.password_out_limit()

    elif len(str(password)) < public_platform.pwd_len_lower_limit:
        return StateConstants.password_less_length()

    elif not re.match(public_platform.mail_regex_rule, str(email)):
        return StateConstants.invalid_email()

    elif any(c in str(email) for c in public_platform.illegal_chars):
        return StateConstants.illegal_char()

    return login_check(email, password)


def login_check(email, commit_password):
    user_row = account_crud.select_user_by_email(email)
    print("user_row", user_row)

    if user_row == None:
        # 检查是否有此账户
        return StateConstants.no_such_user()

    if kwd_pair(user_row, commit_password) < 0:
        return StateConstants.password_incorrect()  # 密码错误

    print("login_check.user_row: ", user_row)
    id = user_row[0]

    response = generate_response(email, id)
    return response


def kwd_pair(user_tuple, commit_password):
    cipher_txt = user_tuple[2]
    private_salt = user_tuple[3]

    local_kwd = cryptography.aes_decrypt(private_salt, cipher_txt)
    print("local_kwd:  ", local_kwd)

    if commit_password != local_kwd:
        return -1
    return 1


def generate_response(email, id):
    params = {"id": id, "email": email}
    response = StateConstants.success()

    token = token_service.create_token(params)
    token_dict = {"token": token}

    response.update(token_dict)
    print("generate_response:  ", response)
    return response


# result = logining_deals_service("title@yon.com", "9999999")
# print("logining result", result)
