import json
import records
import token_service
from state_consts import StateConstants
import fuzzy_title_pagin_search_service


def pagin_search_title_controller(request):
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
    article_title = data_dict.get("title", None)
    page_order = data_dict.get("page_order", 1)

    result = fuzzy_title_pagin_search_service.fuzzy_title_pagin_search_service(
        email, uid, page_order, article_title
    )
    return result
