import re
import essay_crud
from state_consts import StateConstants
import public_platform as pub
import check_params as cek
import cont_cipher


def read_decrypt_blog_service(mail: str, uid: int, article_id: int, key: str):
    if type(mail) != str or type(uid) != int or type(article_id) != int:
        return StateConstants.parameter_invaild_type()

    params_valid = cek.check_params(mail, uid, article_id, key)
    if params_valid == False:
        return StateConstants.param_empty()

    if len(str(mail)) > pub.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(pub.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    if is_contain_chinese(str(key)) == True and str(key) is not None:
        return StateConstants.not_support_chn_key()

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

    res_dict = list2Dictionary(article_list)
    results = {"article": res_dict}

    success = StateConstants.success()
    return {**success, **results}


def is_contain_chinese(string):
    if re.search(pub.chinese_regex, string):
        return True
    else:
        return False


def list2Dictionary(article_list):
    essay_dict = dict()
    essay_dict["articleid"] = article_list[0]
    essay_dict["title"] = article_list[1]
    essay_dict["content"] = article_list[2]
    # essay_dict["userid"] = article_list[3]
    # essay_dict["usermail"] = article_list[4]
    essay_dict["encryption"] = article_list[5]
    essay_dict["level"] = article_list[6]
    essay_dict["time"] = article_list[7]
    return essay_dict


# result = read_decrypt_blog_service("inspector@qq.com", 11, 68, 777)
# print("view_separate_blog_service: ", result)
