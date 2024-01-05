from flask import request, render_template

import logining_controller
import alter_password_controller
import modified_mail_controller
import register_controller

import pagin_blog_entry_controller
import pagin_search_title_controller
import read_separate_controller
import transform_journal_controller
import increase_article_controller
import delete_journal_controller

from state_consts import StateConstants
from app_factory import create_app
import records

app = create_app()


@app.route("/")
def page_login():
    request_record()
    return logining_controller.index_page()


@app.route("/account-login", methods=["GET", "POST"])
def handler_login():
    if request.method == "POST":
        return logining_controller.logining_controller(request)
    elif request.method == "GET":
        return StateConstants.doubt_method()


@app.route("/account-navigation-page")
def page_navigation():
    return render_template("account/navigation.html")


@app.route("/account")
def page_register():
    return register_controller.get_register_page()


@app.route("/account-register", methods=["GET", "POST"])
def handler_register():
    if request.method == "POST":
        return register_controller.register_controller(request)
    elif request.method == "GET":
        return StateConstants.doubt_method()


@app.route("/account-modify-email-page")
def page_modify_email():
    return modified_mail_controller.modified_page()


@app.route("/account-modify-email", methods=["GET", "POST"])
def handler_modify_email():
    if request.method == "POST":
        return modified_mail_controller.modified_email_controller(request)
    elif request.method == "GET":
        return StateConstants.doubt_method()


@app.route("/account-modify-password-page")
def page_modify_password():
    return alter_password_controller.modify_page()


@app.route("/account-modify-password", methods=["GET", "POST"])
def handler_modify_password():
    if request.method == "POST":
        return alter_password_controller.alter_password_controller(request)
    elif request.method == "GET":
        return StateConstants.doubt_method()


@app.route("/essay-blogs-tabulation-page")
def page_blogs_tabulation():
    return pagin_blog_entry_controller.get_pagin_blog_entry_page()


@app.route("/essay-blogs-tabulation", methods=["POST"])
def handler_blogs_tabulation():
    if request.method == "POST":
        return pagin_blog_entry_controller.pagin_blog_entry_controller(request)


@app.route("/essay-search-title", methods=["POST"])
def handler_search_title_blogs():
    if request.method == "POST":
        return pagin_search_title_controller.pagin_search_title_controller(request)


@app.route("/essay-blog-perusal-page")
def page_perusal_single():
    return read_separate_controller.get_blog_perusal_page()


@app.route("/essay-perusal-plain", methods=["POST"])
def handler_perusal_normal():
    if request.method == "POST":
        return read_separate_controller.view_separate_blog_controller(request)


@app.route("/essay-perusal-ciphertext", methods=["POST"])
def handler_perusal_cipher():
    if request.method == "POST":
        return read_separate_controller.read_decrypt_blog_controller(request)


@app.route("/essay-modify-cipher", methods=["POST"])
def handler_modified_cipher():
    if request.method == "POST":
        return transform_journal_controller.transform_cipher_journal_controller(request)


@app.route("/essay-modify-plain", methods=["POST"])
def handler_modified_plain():
    if request.method == "POST":
        return transform_journal_controller.transform_plain_journal_controller(request)


@app.route("/essay-blog-uplift-page")
def page_augment():
    return increase_article_controller.get_blog_uplift_page()


@app.route("/essay-growth-single", methods=["POST"])
def handler_increase_journal():
    if request.method == "POST":
        return increase_article_controller.increase_blog_controller(request)


@app.route("/essay-delete-multiple", methods=["POST"])
def handler_delete_journal():
    if request.method == "POST":
        return delete_journal_controller.delete_journal_controller(request)


def request_record():
    records.type_msg(
        headers=request.headers,
        method=request.method,
        referrer=request.referrer,
        user_agent=request.user_agent,
        base_url=request.base_url,
        url=request.url,
        remote_addr=request.remote_addr,
        url_root=request.url_root,
        path=request.path,
    )


if __name__ == "__main__":
    # 允许 127.0.0.1:port、内网:port、外网:port 访问 flask 接口
    app.run(host="0.0.0.0", port=8085, debug=True)  # 定义app在某个端口运行
