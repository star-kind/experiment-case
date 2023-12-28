import re
import essay_crud
from state_consts import StateConstants
import public_platform
import check_params as cek
import cont_cipher


def read_decrypt_blog_service(mail: str, uid: int, article_id: int, key: str):
    if type(mail) != str or type(uid) != int or type(article_id) != int:
        return StateConstants.parameter_invaild_type()

    params_valid = cek.check_params(mail, uid, article_id, key)
    if params_valid == False:
        return StateConstants.param_empty()

    if len(str(mail)) > public_platform.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(public_platform.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    result_check = cek.account_check_by_mail(mail)
    if result_check.get("flag", "Default") == False:
        return StateConstants.no_such_user()

    user_tuple = result_check.get("user", "DefaultString")

    # if user_id != uid
    if user_tuple[0] != uid:
        return StateConstants.user_status_amiss()

    article_tuple = essay_crud.get_essay_by_essay_id(article_id)
    print("article_tuple: ", article_tuple)

    if article_tuple == None:
        return StateConstants.no_such_essay()

    if article_tuple[5] == 0:
        return StateConstants.not_encrypt_article()

    # if article.user.id != uid or article.user.email != mail
    if article_tuple[3] != uid or article_tuple[4] != mail:
        return StateConstants.user_status_amiss()

    try:
        decrypt_content = cont_cipher.decrypt(str(key), article_tuple[2])
    except ValueError as e:
        if "Padding is incorrect." in str(e):
            return StateConstants.article_key_mismatch()
        else:
            raise e

    article_list = list(article_tuple)
    article_list[2] = decrypt_content

    return StateConstants.success() | {"article": article_list}


# result = read_decrypt_blog_service("testUser@yon.com", 6, 58, 777)
# print("read_decrypt_blog_service: ", result)
