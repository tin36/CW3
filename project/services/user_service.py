from project.tools.security import generate_password_digest, compare_passwords, create_access_token, create_refresh_token, decode_token
from project.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao


    def create(self, user_d):
        user_d["password"] = generate_password_digest(user_d.get("password"))
        return self.dao.create(user_d)

    def user_update(self, data_j, data_r):

        data = decode_token(data_r.split("Bearer ")[-1])
        email = data.get("email")

        return self.dao.update(data_j, email)

    def change_passwords(self, data_p, data_r):

        data_t = decode_token(data_r.split("Bearer ")[-1])
        email = data_t.get("email")
        new_password = data_p.get("new_password")
        old_password = data_p.get("old_password")

        user = self.dao.get_by_username(email)

        try:

            if compare_passwords(user.password, old_password) == True:
                data_p["new_password"] = generate_password_digest(new_password)
                self.dao.update_password(data_p, email)
            else:
                return "Пароли не одинаковые"

        except Exception as e:
            return f"{e} - err"

    def create_tokens(self, data):

        email = data.get("email", None)
        password = data.get("password", None)

        try:
            data_user = self.dao.get_by_username(email)
            if compare_passwords(data_user.password, password) == True:

                data_dict = {
                    "email": data_user.email
                }

                access_token = create_access_token(data_dict)
                refresh_token = create_refresh_token(data_dict)


                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token

                }
            return f"Неверная пара: логин/пароль"

        except Exception as e:
            return f"{e} - err"

    def create_new_tokens(self, data):
        try:
            access_token = data.get("access_token", None)
            refresh_token = data.get("refresh_token", None)

            data_access_token = decode_token(access_token)
            data_refresh_token = decode_token(refresh_token)

            if data_access_token.get("email") == data_refresh_token.get("email"):
                access_token = create_access_token(data_access_token)
                refresh_token = create_refresh_token(data_refresh_token)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token

                }
        except Exception as e:
            return f"{e} - err"




