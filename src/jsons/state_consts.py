class StateConstants:
    @staticmethod
    def success():
        response = {"state": 200, "message": "Successful"}
        return response

    @staticmethod
    def doubt_method():
        response = {"state": 422, "message": "Doubtful Method"}
        return response

    @staticmethod
    def pwd_inconsistent():
        response = {
            "state": 423,
            "message": "The new password entered twice is different",
        }
        return response

    @staticmethod
    def param_empty():
        response = {"state": 424, "message": "Parameters can not was empty"}
        return response

    @staticmethod
    def contains_spaces():
        response = {
            "state": 424,
            "message": "Error: Your commit parameter contains spaces",
        }
        return response

    @staticmethod
    def email_out_limit():
        response = {
            "state": 425,
            "message": "Error: Email length is can not greater than upper limit",
        }
        return response

    @staticmethod
    def password_out_limit():
        response = {
            "state": 426,
            "message": "Error: password length can not greater than upper limit",
        }
        return response

    @staticmethod
    def password_less_length():
        response = {
            "state": 427,
            "message": "Error: password length can not less than lower limit",
        }
        return response

    @staticmethod
    def invalid_email():
        response = {"state": 428, "message": "Error: Invalid email address format"}
        return response

    @staticmethod
    def illegal_char():
        response = {
            "state": 429,
            "message": "Error: Your commit parameter contains invalid characters",
        }
        return response

    @staticmethod
    def no_such_user():
        response = {"state": 430, "message": "Error: No such account"}
        return response

    @staticmethod
    def password_incorrect():
        response = {"state": 431, "message": "Error: Login Password is incorrect"}
        return response

    @staticmethod
    def already_registered():
        response = {
            "state": 432,
            "message": "Error: This email has already been registered by someone",
        }
        return response

    @staticmethod
    def login_expire():
        response = {
            "state": 433,
            "message": "Error: Login status has expired, please login retry",
        }
        return response

    @staticmethod
    def consistent_email():
        response = {
            "state": 434,
            "message": "Error: The replaced email is consistent with the original email",
        }
        return response

    @staticmethod
    def pwd_contain_space():
        response = {"state": 435, "message": "Error: Passwords contains a space"}
        return response

    @staticmethod
    def user_status_amiss():
        response = {
            "state": 436,
            "message": "Error: Your login status was amiss, please login retry",
        }
        return response

    @staticmethod
    def origin_password_incorrect():
        response = {"state": 437, "message": "Error: Original password is incorrect"}
        return response

    @staticmethod
    def parameter_invaild_type():
        response = {"state": 438, "message": "Error: Invaild parameter type"}
        return response

    @staticmethod
    def no_such_essay():
        response = {"state": 439, "message": "No such this article"}
        return response

    @staticmethod
    def not_encrypt_article():
        response = {"state": 440, "message": "The article is not encrypted"}
        return response

    @staticmethod
    def article_key_mismatch():
        response = {"state": 441, "message": "The secret key of article does mismatch"}
        return response
