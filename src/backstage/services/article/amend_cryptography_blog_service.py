import re
import essay_crud
from state_consts import StateConstants
import public_platform
import check_params as cek
import cont_cipher


def amend_cryptography_blog_service(
    uid: int,
    mail: str,
    new_title: str,
    new_content: str,
    article_id: int,
    secret_key: str,
):
    if type(mail) != str or type(uid) != int or type(article_id) != int:
        return StateConstants.parameter_invaild_type()

    clean_title = str(new_title).replace(" ", "")
    clean_content = str(new_content).replace(" ", "")
    clean_secret_key = str(secret_key).replace(" ", "")
    params_valid = cek.check_params(
        mail, uid, clean_title, clean_content, article_id, clean_secret_key
    )
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

    # if article.user.id != uid or article.user.email != mail
    if article_tuple[3] != uid or article_tuple[4] != mail:
        return StateConstants.user_status_amiss()

    if " " in str(secret_key).strip():
        return StateConstants.contains_spaces()

    if secret_key != None or clean_secret_key != "":
        new_cryptography = cont_cipher.encrypt(
            clean_secret_key, str(new_content).strip()
        )

    return generate_response(
        article_id, str(new_title).strip(), new_cryptography.strip(), clean_secret_key
    )


def generate_response(article_id, new_title: str, new_content: str, secret_key: str):
    essay_crud.update_essay_by_id(new_title, new_content, article_id, secret_key)
    return StateConstants.success()


# uid = 6
# mail = "testUser@yon.com"
# new_title = 999
# new_content = 60355265
# article_id = 48
# secret_key = 888999

# result = amend_cryptography_blog_service(
#     uid, mail, new_title, new_content, article_id, secret_key
# )
# print("result", result)
