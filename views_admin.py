from flask import Blueprint
from flask_restful import Api, Resource

# Importing Resources from resources/
from resources.admin.user import UserListResource, UserResource
from resources.admin.authentication import LoginResource
from resources.admin.authentication import SignupResource

apiBp = Blueprint('api', __name__)
api = Api(apiBp)

api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserListResource, '/users/')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')