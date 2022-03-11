from flask_restx import abort, Namespace, Resource
from project.exceptions import ItemNotFound
from project.done import movie_service
from flask import request

movie_ns = Namespace("movies")


@movie_ns.route("/")
class MoviesView(Resource):
    @movie_ns.response(200, "OK")
    def get(self):
        '''Получение всех фильмов'''
        status = request.args.get("status")
        page = request.args.get("page")
        filters = {
            "status": status,
            "page": page
        }

        return movie_service.get_all(filters)


@movie_ns.route("/<int:id>")
class MovieView(Resource):
    @movie_ns.response(200, "OK")
    @movie_ns.response(404, "Фильм не найден")
    def get(self, id: int):
        '''Получение фильма по id'''
        try:
            return movie_service.get_item_by_id(id)
        except ItemNotFound:
            abort(404, message="Фильм не найден")
