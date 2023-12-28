import re
from flask import render_template
import records
from state_consts import StateConstants
import token_service
import cryptography
import account_crud
import modified_email_service


def modified_page(request):
    html_path = "account/ModifyEmail.html"
    print("modified_page.request.headers: ", request.headers)
    return render_template(html_path)


def modified_email_controller(request):
    records.type_msg(handler_modified_email_form=request.form)
    new_email = request.form["new_email"]
    password = request.form["password"]

    token_str = token_service.get_token_from_req(request)
    resp = token_service.verify_get_usr_data(token_str)

    flag = resp.get("flag", "default_value")
    if flag == False:
        return StateConstants.login_expire()

    origin_email = resp.get("email", "defaultEmail")
    records.type_msg(Origin_email=origin_email)

    return modified_email_service.modified_email_service(
        new_email, password, origin_email
    )
