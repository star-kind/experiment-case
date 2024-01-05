import execute_sentence
import explore_tables
import public_platform as pub


def create_essay_tbl():
    sentence = """CREATE TABLE IF NOT EXISTS essay (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    account_id INTEGER NOT NULL,
    account_email TEXT NOT NULL,
    modification_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notch INTEGER NOT NULL DEFAULT 0,
    is_encrypted INTEGER NOT NULL DEFAULT 0
    );"""
    execute_sentence.execute_no_result(sentence, ())
    explore_tables.explore_tables()


# create_essay_tbl()


def inserts_essay(title, content, account_id, account_email, encrypted_key):
    sentence = (
        "INSERT INTO essay (title,content,account_id,account_email) VALUES (?,?,?,?);"
    )

    sentence1 = "INSERT INTO essay (title,content,account_id,account_email,is_encrypted) VALUES (?,?,?,?,?);"

    if encrypted_key == None or encrypted_key == "":
        create_essay_tbl()
        execute_sentence.execute_no_result(
            sentence, (title, content, account_id, account_email)
        )
    else:
        create_essay_tbl()
        execute_sentence.execute_no_result(
            sentence1,
            (
                title,
                content,
                account_id,
                account_email,
                pub.encrypted_rating,
            ),
        )


# inserts_essay("title 1", "content 111", 1, "account_email@rso.com", 1)
# inserts_essay("title 000", "content 999", 2, "account@email.com", None)
# for i in range(21):
#     inserts_essay(
#         "title 000." + str(i * 88),
#         "content 999." + str(i * 88),
#         3,
#         "account@email.com",
#         None,
#     )


def select_all_essays():
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(sentence, ())
    return results


# select_all_essays()


def select_essay_by_mail(email):
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_email = ? ;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(sentence, (email,))
    return results


# select_essay_by_mail("account@email.com")


def select_essay_by_uid(uid):
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_id = ? ;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(sentence, (uid,))
    return results


# select_essay_by_uid(3)


def get_essay_by_essay_id(id):
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE id = ? ;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_one_row(sentence, (id,))
    return results


# get_essay_by_essay_id(9)


def paginate_essay_by_uid(account_id, rows_size, page_number):
    # 计算分页的起始索引
    start_index = (page_number - 1) * rows_size

    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_id = ? ORDER BY id DESC LIMIT ? OFFSET ?;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(
        sentence, (account_id, rows_size, start_index)
    )
    return results


# paginate_essay_by_uid(2, 5, 2)


def paginate_essay_by_mail(account_mail, rows_size, page_number):
    # 计算分页的起始索引
    start_index = (page_number - 1) * rows_size

    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_email = ? ORDER BY id DESC LIMIT ? OFFSET ?;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(
        sentence, (account_mail, rows_size, start_index)
    )
    return results


def total_fuzzy_title_by_uid(search_title, uid):
    # 执行分页查询，包含WHERE条件并按id倒序排列
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_id = ? AND title LIKE ? ORDER BY id;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(
        sentence, (uid, f"%{search_title}%")
    )
    return results


def paginate_fuzzy_title_by_uid(page_number, rows_size, search_title, uid):
    start_index = (page_number - 1) * rows_size

    # 执行分页查询，包含WHERE条件并按id倒序排列
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_id = ? AND title LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(
        sentence, (uid, f"%{search_title}%", rows_size, start_index)
    )
    return results


# paginate_fuzzy_title_by_uid(2, 5, "title", 2)


def total_fuzzy_title_by_mail(search_title, mail):
    # 执行分页查询，包含WHERE条件并按id倒序排列
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_email = ? AND title LIKE ? ORDER BY id DESC;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(
        sentence, (mail, f"%{search_title}%")
    )
    return results


def paginate_fuzzy_title_by_mail(page_number, rows_size, search_title, mail):
    start_index = (page_number - 1) * rows_size

    # 执行分页查询，包含WHERE条件并按id倒序排列
    sentence = "SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time FROM essay WHERE account_email = ? AND title LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?;"

    create_essay_tbl()
    results = execute_sentence.execute_fetch_records(
        sentence, (mail, f"%{search_title}%", rows_size, start_index)
    )
    return results


# paginate_fuzzy_title_by_mail(2, 5, "title", "account@email.com")


def update_essay_by_id(title, content, id, encrypt_key: str):
    sentence = "UPDATE essay SET title = ?, content = ?, is_encrypted = ?, modification_time = CURRENT_TIMESTAMP WHERE id = ?;"

    create_essay_tbl()
    if encrypt_key == None or encrypt_key.replace(" ", "") == "":
        execute_sentence.execute_no_result(
            sentence, (title, content, pub.plaintext_rating, id)
        )
    else:
        execute_sentence.execute_no_result(
            sentence, (title, content, pub.encrypted_rating, id)
        )


# update_essay_by_id("new title 9090", "new content 8090", 12, None)
# get_essay_by_essay_id(12)
# update_essay_by_id("new title R0R8", "new content R0R8 R0R8", 11, 99)
# get_essay_by_essay_id(11)


def deleted_essay_by_id(id):
    sentence = "DELETE FROM essay WHERE id = ?;"

    create_essay_tbl()
    execute_sentence.execute_no_result(sentence, (id,))


# deleted_essay_by_id(12)
# get_essay_by_essay_id(12)


def get_latest_insert_essay(email, uid, title, encrypted_rating):
    sentence = f"""SELECT id,title,content,account_id,account_email,is_encrypted,notch,modification_time 
    FROM essay 
    WHERE account_email = ? 
    AND account_id = ? 
    AND title = ? 
    AND is_encrypted = ? 
    ORDER BY id DESC
    LIMIT 1;
    """

    create_essay_tbl()
    row = execute_sentence.execute_fetch_one_row(
        sentence, (email, uid, title, encrypted_rating)
    )
    return row
