from project.dao.models.base import BaseMixin
from project.setup_db import db
from project.dao.models.director import Director
from project.dao.models.genre import Genre


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"

    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey(Genre.id))
    # genre = db.relationship(Genre)
    director_id = db.Column(db.Integer, db.ForeignKey(Director.id))
    # director = db.relationship(Director)

    def __repr__(self):
        return f"<Movie '{self.title.title()}'>"
