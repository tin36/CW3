from project.dao.models.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session


    def get_by_username(self, email):
        return self.session.query(User).filter(User.email == email).first()




    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user_d, email):
        user = self.get_by_username(email)
        user.name = user_d.get("name")
        user.surname = user_d.get("surname")
        user.favourite_genre = user_d.get("favourite_genre")


        self.session.add(user)
        self.session.commit()



    def update_password(self, user_p, email):
        user = self.get_by_username(email)
        user.password = user_p.get("new_password")

        self.session.add(user)
        self.session.commit()

