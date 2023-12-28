import re
import essay_crud
from state_consts import StateConstants
import public_platform as pub
import check_params as cek
from pagination import Pagination


def pagin_search_service(mail: str, uid, page_order):
    params_valid = cek.check_params(mail, uid, page_order)
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

    data = generate_response(mail, page_order)
    return StateConstants.success() | {"pagination": data}


def generate_response(mail, page_order):
    # get total rows
    total_lines = essay_crud.select_essay_by_mail(mail)

    # get pagin data
    pagin_data = essay_crud.paginate_essay_by_mail(mail, pub.rows_per_page, page_order)

    pagin_dictionary = Pagination(
        total_rows=len(total_lines),
        rows_per_page=pub.rows_per_page,
        current_page=page_order,
    )

    pagin_dictionary._paged_data = pagin_data
    return pagin_dictionary.to_dictionary()


# result = pagin_search_service("testUser@yon.com", 6, 1)
# print("pagin_search_service: ", result)
