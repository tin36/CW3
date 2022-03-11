from sqlalchemy.orm.scoping import scoped_session

from project.dao.models.movie import Movie

class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self, filters):
        t = self._db_session.query(Movie)
        if filters.get("status") == "new" and filters.get("page") is not None:
            t = t.order_by(Movie.year.desc()).limit(12).offset((int(filters["page"]) - 1) * 12)
        elif filters.get("status") == "new":
            t = t.order_by(Movie.year.desc())
        elif filters.get("page") is not None:
            t = t.limit(12).offset((int(filters["page"]) - 1) * 12)
        return t.all()
 #       return self._db_session.query(Movie).all()
