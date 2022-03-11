from flask_restx import Resource, Namespace
from flask import request
from project.done import user_service
from project.tools.security import auth_required

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):

    @auth_required
    def get(self):
        return "", 200

    @auth_required
    def patch(self):
        user_d = request.json
        data_r = request.headers['Authorization']

        return user_service.user_update(user_d, data_r), 204




@user_ns.route('/password')
class UserPassView(Resource):

    @auth_required
    def put(self):
        user_p = request.json
        data_r = request.headers['Authorization']
        user_service.change_passwords(user_p, data_r)

        return user_service.change_passwords(user_p, data_r), 204


