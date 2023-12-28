import re
import essay_crud
from state_consts import StateConstants
import public_platform as pub
import check_params as cek
from pagination import Pagination


def fuzzy_title_pagin_search_service(mail: str, uid, page_order, title: str):
    params_valid = cek.check_params(mail, uid, page_order, title)
    if params_valid == False:
        return StateConstants.param_empty()

    if len(str(mail)) > pub.mail_len_upper_limit:
        return StateConstants.email_out_limit()

    if not re.match(pub.mail_regex_rule, str(mail)):
        return StateConstants.invalid_email()

    if type(mail) != str or type(page_order) != int or type(uid) != int:
        return StateConstants.parameter_invaild_type()

    result_check = cek.account_check_by_mail(mail)
    if result_check.get("flag", "Default") == False:
        return StateConstants.no_such_user()

    user_tuple = result_check.get("user", "DefaultString")
    # if user_id != uid
    if user_tuple[0] != uid:
        return StateConstants.user_status_amiss()

    data = generate_response(mail, page_order, title)
    return StateConstants.success() | {"pagination": data}


def generate_response(mail, page_order, title):
    # get total rows
    total_lines = essay_crud.total_fuzzy_title_by_mail(title, mail)

    # get pagin data
    pagin_data = essay_crud.paginate_fuzzy_title_by_mail(
        page_order, pub.rows_per_page, title, mail
    )

    pagin_dictionary = Pagination(
        total_rows=len(total_lines),
        rows_per_page=pub.rows_per_page,
        current_page=page_order,
    )

    pagin_dictionary._paged_data = pagin_data
    return pagin_dictionary.to_dictionary()


# result = fuzzy_title_pagin_search_service("testUser@yon.com", 6, 1, 999)
# print("fuzzy_title_pagin_search_service: ", result)
