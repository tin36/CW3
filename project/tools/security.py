import base64
import hashlib
import hmac
import datetime
import calendar
import jwt
from flask import abort, request
from flask import current_app


def generate_password_digest(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"]
    ))



def compare_passwords(password_hash, other_password) -> bool:
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac('sha256', other_password.encode(),
                            current_app.config["PWD_HASH_SALT"], current_app.config["PWD_HASH_ITERATIONS"])
    )


def create_access_token(data_dict):
    mins30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data_dict["exp"] = calendar.timegm(mins30.timetuple())
    access_token = jwt.encode(data_dict, current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGO"])

    return access_token

def create_refresh_token(data_dict):
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data_dict["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data_dict, current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGO"])

    return refresh_token

def decode_token(token):

    decode_data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])

    return decode_data


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]


        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])

        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


