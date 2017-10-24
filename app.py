from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import config

application = Flask(__name__)
CORS(application)
api = Api(application)

application.config['SQLALCHEMY_DATABASE_URI'] = config.db_url

db = SQLAlchemy(application)

from api import VdiClient, Register, Connection, User, Login, Blueprint

api.add_resource(VdiClient, '/vdi', endpoint="VdiClients")
api.add_resource(VdiClient, '/vdi/<id>')
api.add_resource(Register, '/register')
api.add_resource(Connection, '/token', endpoint = "tokens")
api.add_resource(Connection, '/token/<id>', endpoint="token")
api.add_resource(User, '/user')
api.add_resource(User, '/user/<id>', endpoint="users")
api.add_resource(Login, '/login')
api.add_resource(Blueprint, '/blueprint')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8000', debug=True)
