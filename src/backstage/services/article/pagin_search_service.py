import re
import essay_crud
from state_consts import StateConstants
import public_platform as pub
import check_params as cek
from pagination import Pagination


def pagin_search_service(mail: str, uid, page_order):
    params_valid = cek.check_params(mail, uid)
    if params_valid == False:
        return StateConstants.param_empty()

    if len(str(mail)) > pub.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(pub.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    if type(mail) != str or type(page_order) != int or type(uid) != int:
        return StateConstants.parameter_invaild_type()

    if page_order < 1:
        return StateConstants.already_first_page()

    result_check = cek.account_check_by_mail(mail)
    if result_check.get("flag", "Default") == False:
        return StateConstants.no_such_user()

    user_tuple = result_check.get("user", "DefaultString")
    # if user_id != uid
    if user_tuple[0] != uid:
        return StateConstants.user_status_amiss()

    data = generate_response(mail, page_order)

    if page_order > data["total_pages"]:
        return StateConstants.already_last_page()
    else:
        pagin_dict = {"pagination": data}
        success = StateConstants.success()
        return {**success, **pagin_dict}


def generate_response(mail, page_order):
    # get total rows
    total_lines = essay_crud.select_essay_by_mail(mail)

    # get pagin data
    pagin_data = essay_crud.paginate_essay_by_mail(mail, pub.rows_per_page, page_order)
    results_pagin = ergodic_tuple(pagin_data)

    pagin_dictionary = Pagination(
        total_rows=len(total_lines),
        rows_per_page=pub.rows_per_page,
        current_page=page_order,
    )

    pagin_dictionary._paged_data = results_pagin
    pagin_dict = pagin_dictionary.to_dictionary()
    # print("pagin_dict", pagin_dict)
    return pagin_dict


def ergodic_tuple(two_dim_tuple):
    rows_list = list()
    # 遍历二维元组
    for i, row in enumerate(two_dim_tuple):
        article_dict = dict()
        for j, element in enumerate(row):
            # print(f"tuple[{i}][{j}] = {element}")
            switch_case(j, element, article_dict)
        rows_list.append(article_dict)

    return rows_list


def switch_case(index, value, article_dict):
    if index == 0:
        article_dict["articleid"] = value
    elif index == 1:
        article_dict["title"] = value
    elif index == 2:
        article_dict["content"] = ""
    elif index == 3:
        article_dict["uid"] = ""
    elif index == 4:
        article_dict["mailbox"] = value
    elif index == 5:
        article_dict["encryption"] = value
    elif index == 6:
        article_dict["scale"] = value
    elif index == 7:
        article_dict["time"] = value


def test():
    mailbox = "Register@qq.com"
    userid = 1
    page_number = 1
    result = pagin_search_service(mailbox, userid, page_number)
    print("pagin_search_service: ", result)


# test()
