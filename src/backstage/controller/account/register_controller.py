from flask import render_template

import records
import register_service


def get_register_page():
    html_path = "account/register.html"
    return render_template(html_path)


def register_controller(request_data):
    records.type_msg(register_controller=request_data.form)
    email = request_data.form["email"]
    password = request_data.form["password"]
    re_password = request_data.form["repeat_password"]
    return register_service.register_deals_service(email, password, re_password)
