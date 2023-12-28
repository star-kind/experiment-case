from flask import render_template

import records
import register_service


def get_register_page():
    html_path = "account/register.html"
    return render_template(html_path)


def handle_register_data(request_data):
    records.type_msg(handle_register_data_request_dataForm=request_data.form)
    return register_process(request_data)


def register_process(request_data):
    email = request_data.form["email"]
    password = request_data.form["password"]
    re_password = request_data.form["repeat_password"]
    return register_service.register_deals_service(email, password, re_password)
