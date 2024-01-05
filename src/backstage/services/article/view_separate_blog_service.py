import re
import essay_crud
from state_consts import StateConstants
import public_platform
import account_crud
import check_params as cek


def view_separate_blog_service(mail: str, uid: int, article_id: int):
    if type(mail) != str or type(uid) != int or type(article_id) != int:
        return StateConstants.parameter_invaild_type()

    params_valid = cek.check_params(mail, uid, article_id)
    if params_valid == False:
        return StateConstants.param_empty()

    if len(str(mail)) > public_platform.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(public_platform.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    result_check = account_check(mail)
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

    # if article.user.id != uid or article.user.email != mail
    if article_tuple[3] != uid or article_tuple[4] != mail:
        return StateConstants.user_status_amiss()

    article_list = list(article_tuple)
    result_dictionary = list2Dictionary(article_list)
    return StateConstants.success() | {"article": result_dictionary}


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


def account_check(email):
    user_row = account_crud.select_user_by_email(email)
    print("user_row", user_row)

    if user_row == None:
        # 检查是否有此账户
        return {"flag": False, "user": None}
    else:
        return {"flag": True, "user": user_row}


# result = view_separate_blog_service("inspector@qq.com", 11, 68)
# print("view_separate_blog_service: ", result)
