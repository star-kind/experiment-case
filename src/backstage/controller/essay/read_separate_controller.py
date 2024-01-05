import view_separate_blog_service
import read_decrypt_blog_service

import json
import records
import token_service
from state_consts import StateConstants
from flask import render_template


def get_blog_perusal_page():
    html_path = "essay/perusal-journal.html"
    return render_template(html_path)


def view_separate_blog_controller(request):
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
    article_id = data_dict.get("article_id", None)

    result = view_separate_blog_service.view_separate_blog_service(
        email, uid, article_id
    )
    return result


def read_decrypt_blog_controller(request):
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
    article_id = data_dict.get("article_id", None)
    article_key = data_dict.get("article_key", None)

    result = read_decrypt_blog_service.read_decrypt_blog_service(
        email, uid, article_id, article_key
    )
    return result
