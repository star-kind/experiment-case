import re
import essay_crud
from state_consts import StateConstants
import public_platform as pub
import account_crud
import cont_cipher
import check_params as chk


def write_blog_service(title: str, content: str, mail: str, uid: int, encrypt_key: str):
    if type(uid) != int:
        return StateConstants.parameter_invaild_type()

    clean_content = str(content).replace(" ", "")
    clean_title = str(title).replace(" ", "")
    if chk.check_params(clean_title, clean_content, mail, uid) == False:
        return StateConstants.param_empty()

    if len(str(mail)) > pub.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(pub.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    if is_contain_chinese(str(encrypt_key)) == True and str(encrypt_key) is not None:
        return StateConstants.not_support_chn_key()

    result_check = user_check(mail)
    if result_check.get("flag", "Default") == False:
        return StateConstants.no_such_user()

    user_tuple = result_check.get("user", "DefaultString")

    # if user_id != uid
    if user_tuple[0] != uid:
        return StateConstants.user_status_amiss()

    reciprocate = encrypt_provided(encrypt_key, content)
    print("reciprocate: ", reciprocate)

    return shapeResponse(reciprocate, title, content, uid, mail, encrypt_key)


def shapeResponse(reciprocate, title, content, uid, mail, encrypt_key):
    if reciprocate == None:
        essay_crud.inserts_essay(
            str(title).strip(), str(content).strip(), uid, mail, None
        )
        row_tuple = essay_crud.get_latest_insert_essay(
            mail, uid, title, pub.plaintext_rating
        )

        result_dict = tuple2dictionary(row_tuple)
        return StateConstants.success() | {"review": result_dict}
    else:
        essay_crud.inserts_essay(
            str(title).strip(),
            str(reciprocate).strip(),
            uid,
            mail,
            str(encrypt_key).strip(),
        )
        row_tuple = essay_crud.get_latest_insert_essay(
            mail, uid, title, pub.encrypted_rating
        )

        result_dict = tuple2dictionary(row_tuple)
        return StateConstants.success() | {"review": result_dict}


def tuple2dictionary(mine_tuple):
    mine_dict = {}
    mine_dict["articleid"] = mine_tuple[0]
    mine_dict["title"] = mine_tuple[1]
    mine_dict["content"] = mine_tuple[2]
    mine_dict["encryption"] = mine_tuple[5]
    mine_dict["level"] = mine_tuple[6]
    mine_dict["time"] = mine_tuple[7]
    return mine_dict


def encrypt_provided(encrypt_key, content):
    if (
        encrypt_key is not None
        and str(encrypt_key) != ""
        and not str(encrypt_key).isspace()
    ):
        key_str = str(encrypt_key).strip()
        reciprocate = cont_cipher.encrypt(key_str, str(content).strip())
        return reciprocate
    else:
        return None


def user_check(email):
    user_row = account_crud.select_user_by_email(email)
    print("user_row", user_row)

    if user_row == None:
        # 检查是否有此账户
        return {"flag": False, "user": None}
    else:
        return {"flag": True, "user": user_row}


def is_contain_chinese(string):
    if re.search(pub.chinese_regex, string):
        return True
    else:
        return False


def test():
    title = "标题 example "
    content = "正文 测试test 日志 "
    uid = 1
    mail = "punter@qq.com"
    encrypt_str = "hi 文"
    for i in range(2):
        title = title + str(i * 2)
        content = content + str(i * 3)
        result = write_blog_service(title, content, mail, uid, encrypt_str)
    print("result", result)


# test()
