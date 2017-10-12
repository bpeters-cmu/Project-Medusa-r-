from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import config

application = Flask(__name__)
api = Api(application)

application.config['SQLALCHEMY_DATABASE_URI'] = config.db_url

db = SQLAlchemy(application)

from api import VdiClient, Register, Connection, User, Login

api.add_resource(VdiClient, '/vdi')
api.add_resource(Register, '/register')
api.add_resource(Connection, '/token')
api.add_resource(User, '/user')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8000', debug=True)