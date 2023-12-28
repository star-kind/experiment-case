import sys

print(sys.path)

import explore_tables
import execute_sentence


def create_table():
    sentence = """CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE CHECK(length(email) <= 50),
    password TEXT NOT NULL UNIQUE CHECK(length(password) <= 200),
    salt TEXT NOT NULL UNIQUE CHECK(length(salt) <= 200),
    property INTEGER DEFAULT 0,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );"""

    execute_sentence.execute_no_result(sentence, ())
    explore_tables.explore_tables()


# create_table()


def inserts(email, passwd, salt):
    sentence = "INSERT INTO accounts (email,password,salt) VALUES (?,?,?);"

    create_table()
    execute_sentence.execute_no_result(sentence, (email, passwd, salt))


# inserts("emailIIIclk@qq.com", "gosunIoPipasswd999", "fytxtxSwlisalt999")
# inserts("emailIIIUBG@qq.com", "FVYTIoPipasswd999", "citn88Swlisalt999")
# inserts("email666@qq.com", "IoPipasswd99922givid", "Swlisalt999000tis70")


def select_all_user():
    sentence = "SELECT id,email,password,salt,property,update_time FROM accounts;"

    create_table()
    results = execute_sentence.execute_fetch_records(sentence, ())
    return results


# select_all_user()


def select_user_by_email(email):
    create_table()
    sentence = "SELECT id,email,password,salt,property,update_time FROM accounts WHERE email = ? ;"

    create_table()
    results = execute_sentence.execute_fetch_one_row(sentence, (email,))
    return results


# single = select_user_by_email("title@yon.com")
# print("single", type(single))
# print("id", single[0])
# print("cipher", single[2])
# print("salt", single[3])


def select_user_by_id(id):
    sentence = "SELECT id,email,password,salt,property,update_time FROM accounts WHERE id = ? ;"

    create_table()
    results = execute_sentence.execute_fetch_one_row(sentence, (id,))
    return results


# single_usr=select_user_by_id(1)
# print('single usr',single_usr)


def update_email_by_id(new_email, id):
    sentence = (
        "UPDATE accounts SET email = ?, update_time = CURRENT_TIMESTAMP WHERE id = ? ;"
    )

    create_table()
    execute_sentence.execute_no_result(sentence, (new_email, id))


# update_email_by_id('new_email@idc.com',1)
# single_usr=select_user_by_id(1)
# print('single usr',single_usr)


def update_email_by_mail(new_email, origin_mail):
    sentence = "UPDATE accounts SET email = ?, update_time = CURRENT_TIMESTAMP WHERE email = ? ;"

    create_table()
    execute_sentence.execute_no_result(sentence, (new_email, origin_mail))


def update_password_by_id(new_password, id):
    sentence = "UPDATE accounts SET password = ?, update_time = CURRENT_TIMESTAMP WHERE id = ?;"

    create_table()
    execute_sentence.execute_no_result(sentence, (new_password, id))


# update_password_by_id('new-password-yes-sir',1)
# single_usr=select_user_by_id(1)
# print('single usr',single_usr)


def update_password_by_email(new_password, email):
    sentence = "UPDATE accounts SET password = ?, update_time = CURRENT_TIMESTAMP WHERE email = ?;"

    create_table()
    execute_sentence.execute_no_result(sentence, (new_password, email))


# update_password_by_email('new_password.new_password.new_password','emailIIIUBG@qq.com')
# single=select_user_by_email('emailIIIUBG@qq.com')
# print('single',single)
