from flask import render_template

import records
import alter_password_service
import verify_req_token


def modify_page():
    html_path = "account/ModifyPassword.html"
    return render_template(html_path)


def alter_password_controller(req):
    records.type_msg(alter_password_controller=req.form)

    data_dict = verify_req_token.check_token_data(req)
    if data_dict.get("flag", "TrueDefault") == False:
        return data_dict

    user_email = data_dict.get("email", "TrueDefault")

    repeat_new_password = req.form["repeat_new_password"]
    new_password = req.form["new_password"]
    previous_password = req.form["previous_password"]

    return alter_password_service.alter_pwd_service(
        previous_password, new_password, repeat_new_password, user_email
    )
