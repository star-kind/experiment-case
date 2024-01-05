import write_blog_service

import json
import records
import token_service
from state_consts import StateConstants
from flask import render_template


def get_blog_uplift_page():
    html_path = "essay/augment-journal.html"
    return render_template(html_path)


def increase_blog_controller(request):
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
    title = data_dict.get("title", None)
    content = data_dict.get("content", None)
    encrypt_key = data_dict.get("encrypt_key", None)

    result = write_blog_service.write_blog_service(
        title, content, email, uid, encrypt_key
    )
    return result
