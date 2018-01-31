from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import config

application = Flask(__name__)
CORS(application)
api_f = Api(application)

application.config['SQLALCHEMY_DATABASE_URI'] = config.db_url

db = SQLAlchemy(application)

from api import VdiClient, Register, Connection, User, Login, Blueprint

api_f.add_resource(VdiClient, '/vdi', endpoint="VdiClients")
api_f.add_resource(VdiClient, '/vdi/<id>')
api_f.add_resource(Register, '/register')
api_f.add_resource(Connection, '/token', endpoint = "tokens")
api_f.add_resource(Connection, '/token/<id>', endpoint="token")
api_f.add_resource(User, '/user')
api_f.add_resource(User, '/user/<id>', endpoint="users")
api_f.add_resource(Login, '/login')
api_f.add_resource(Blueprint, '/blueprint')

from oci_endpoint import OCILogin, Admin, Instances, Compartments

api_f.add_resource(Admin, '/admin')
api_f.add_resource(OCILogin, '/ocilogin')
api_f.add_resource(Instances, '/instances/<c_ocid>', endpoint = "instances")
api_f.add_resource(Instances, '/instances', endpoint = "instance")
api_f.add_resource(Compartments, '/compartments')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8000', debug=True)
