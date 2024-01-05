import json
import records
import token_service
from state_consts import StateConstants
import revamp_plaintext_blog_service
import amend_cryptography_blog_service


def transform_plain_journal_controller(request):
    records.type_msg(pagin_blog_entry_data=request.data)

    token_str = token_service.get_token_from_req(request)
    resp = token_service.verify_get_usr_data(token_str)

    flag = resp.get("flag", "default_value")
    if flag == False:
        return StateConstants.login_expire()

    email = resp.get("email", "defaultEmail")
    uid = resp.get("id", "defaultID")

    json_bytes = request.data
    print("json_bytes", json_bytes)

    # 先将字节串解码为字符串
    json_str = json_bytes.decode("utf-8")

    # 然后解析JSON字符串为Python对象
    data_dict = json.loads(json_str)
    new_title = data_dict.get("new_title", None)
    new_content = data_dict.get("new_content", None)
    article_id = data_dict.get("article_id", None)

    result = revamp_plaintext_blog_service.revamp_plaintext_blog_service(
        uid, email, new_title, new_content, article_id
    )
    return result


def transform_cipher_journal_controller(request):
    records.type_msg(pagin_blog_entry_data=request.data)

    token_str = token_service.get_token_from_req(request)
    resp = token_service.verify_get_usr_data(token_str)

    flag = resp.get("flag", "default_value")
    if flag == False:
        return StateConstants.login_expire()

    email = resp.get("email", "defaultEmail")
    uid = resp.get("id", "defaultID")

    json_bytes = request.data
    print("json_bytes", json_bytes)

    # 先将字节串解码为字符串
    json_str = json_bytes.decode("utf-8")

    # 然后解析JSON字符串为Python对象
    data_dict = json.loads(json_str)
    new_title = data_dict.get("new_title", None)
    new_content = data_dict.get("new_content", None)
    article_id = data_dict.get("article_id", None)
    secret_key = data_dict.get("secret_key", None)

    result = amend_cryptography_blog_service.amend_cryptography_blog_service(
        uid, email, new_title, new_content, article_id, secret_key
    )
    return result
