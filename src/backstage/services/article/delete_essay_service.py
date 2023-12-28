import re
import essay_crud
from state_consts import StateConstants
import public_platform
import check_params as chk


def delete_essay_service(uid, mail, article_id):
    if type(uid) != int or type(article_id) != int or type(mail) != str:
        return StateConstants.parameter_invaild_type()

    if chk.check_params(uid, mail, article_id) == False:
        return StateConstants.param_empty()

    if len(str(mail)) > public_platform.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(public_platform.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    result_check = chk.account_check_by_mail(mail)
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

    return generate_response(article_id)


def generate_response(article_id):
    essay_crud.deleted_essay_by_id(article_id)
    return StateConstants.success()


# uid = 6
# email = "testUser@yon.com"
# article_id = 50
# result = delete_essay_service(uid, email, article_id)
# print("result", result)
