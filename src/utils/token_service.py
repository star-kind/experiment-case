import datetime
import jwt

import records
from app_factory import create_app
import public_platform

app = create_app()


def create_token(param_body: dict):
    param_body[public_platform.expire_key_name] = (
        int(datetime.datetime.now().timestamp()) + app.config["EXPIRES_IN"]
    )
    app.logger.info("create_token.param_body: " + str(param_body))

    token = None
    try:
        # 使用配置文件中的值
        token = jwt.encode(
            payload=param_body, key=app.config["SECRET_KEY"], algorithm="HS256"
        )
    except Exception as e:
        app.logger.error("获取token失败:{}".format(e))

    app.logger.info("create_token.token: " + str(token))
    return token


def verify_token(token):
    try:
        # 使用SECRET_KEY从配置文件中解码令牌
        decoded_token = jwt.decode(
            token, app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        app.logger.info("verify_token_decoded_token: ", decoded_token)

        # 假设 decoded_token[expire_key_name] 是一个 Unix 时间戳
        expire_time = datetime.datetime.fromtimestamp(
            decoded_token[public_platform.expire_key_name]
        )

        # 检查令牌是否过期
        if datetime.datetime.now() > expire_time:
            return False
        return True

    except jwt.ExpiredSignatureError:
        app.logger.error("Token已过期")
        return False

    except jwt.InvalidTokenError as e:
        app.logger.error("无效的Token: {}".format(e))
        return False


def get_data_by_token(token):
    decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    app.logger.info(str("get_data_by_token_decoded_token: " + str(decoded_token)))
    return decoded_token


def get_token_from_req(request):
    author_str = request.headers.get("Authorization", "Default")
    records.type_msg(request_headersAuthorization=author_str)

    token_str = author_str.replace("Bearer ", "")
    records.type_msg(token_str=token_str)
    return token_str


def verify_get_usr_data(token_string):
    status = verify_token(token_string)

    if status == False:
        return {"flag": status}

    usr_info = get_data_by_token(token_string)
    app.logger.info("Verify_get_usr_data.usr_info: ", usr_info)
    return usr_info
