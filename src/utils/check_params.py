import account_crud


# 遍历所有的参数，对每个参数进行空值检查。如果发现任意一个参数不满足条件，函数会立即返回False。只有当所有参数都满足条件时，函数才会返回True
def check_params(*args):
    for arg in args:
        if not arg:
            return False
    return True


def account_check_by_mail(email):
    user_row = account_crud.select_user_by_email(email)
    print("user_row", user_row)

    if user_row == None:
        # 检查是否有此账户
        return {"flag": False, "user": None}
    else:
        return {"flag": True, "user": user_row}
