import token_service
import records
from state_consts import StateConstants


def check_token_data(request):
    res_dict = {}
    token_str = token_service.get_token_from_req(request)
    resp = token_service.verify_get_usr_data(token_str)

    flag = resp.get("flag", "defaultValue")
    if flag == False:
        res_dict = StateConstants.login_expire() | {"flag": False}

    else:
        user_email = resp.get("email", "defaultEmail")
        user_id = resp.get("id", "defaultID")
        records.type_msg(user_email=user_email, user_id=user_id)
        res_dict = {"email": user_email, "id": user_id, "flag": True}
    return res_dict
