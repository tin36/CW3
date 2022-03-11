from project.dao.movie import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema



class MoviesService():
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_item_by_id(self, pk):
        director = self.dao.get_by_id(pk)
        if not director:
            raise ItemNotFound
        return MovieSchema().dump(director)

    def get_all(self, filters):
        d = {}
        if filters.get("status") is not None:
            movies = self.dao.get_all(filters)
        elif filters.get("page") is not None:
            movies = self.dao.get_all(filters)
        else:
            movies = self.dao.get_all({})
        return MovieSchema(many=True).dump(movies)
