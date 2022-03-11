from flask_restx import Resource, Namespace
from flask import jsonify, make_response, request
from project.done import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        user = request.json
        user_service.create(user)

        return "", 200


@auth_ns.route('/login')
class AuthLoginView(Resource):

    def post(self):
        data = request.json
        tokens = user_service.create_tokens(data)

        return make_response(jsonify(tokens), 201)

    def put(self):
        data = request.json
        tokens = user_service.create_new_tokens(data)

        return make_response(jsonify(tokens), 201)





