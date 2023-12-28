from flask import render_template

import records
import logining_service


def index_page():
    html_path = "account/index.html"
    return render_template(html_path)


def logining_controller(request_data):
    records.type_msg(handle_login_data_request_dataForm=request_data.form)
    email = request_data.form["email"]
    password = request_data.form["password"]
    return logining_service.logining_deals_service(email, password)
