from flask import request, g
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
import traceback
import models

auth = HTTPBasicAuth()

class Login(Resource):
    @auth.login_required
    def get(self):
        return g.user.__tablename__

    @auth.verify_password
    def verify_password(username, password):
        admin = models.Admin.query.filter_by(username = username).first()
        user = models.User.query.filter_by(username = username).first()
        print(user)
        if admin and admin.verify_password(password):
            return True
        if user and user.verify_password(password):
            return True

        return False


class Register(Resource):

    def post(self):
        data = request.get_json(force=True)
        try:
            new_user = models.Admin(data['username'], data['password'], data['ravello_username'],
            data['ravello_password'])
            if new_user.insert():
                return 'OK', 201
            return 'User Create Failed', 400
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400


class VdiClient(Resource):

    @auth.login_required
    def get(self, id=None):
        print('entering get')
        try:
            if not id:

                clients = models.Client.query.filter_by(admin_id=g.user.id)
                data = [c.serialize() for c in clients]
                return data, 200
            else:
                print(id)
                return models.Client.query.get(id).get_token(), 200

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.login_required
    def post(self):
        data = request.get_json(force=True)
        try:
            return g.user.create_clients(data['quantity']), 201

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.login_required
    def put(self, id):
        data = request.get_json(force=True)
        try:
            client = models.Client.query.get(id)
            return client.start_stop(data['action']), 200
        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.login_required
    def delete(self, id):
        print('enter delete')
        try:
            client = models.Client.query.get(id)
            return client.delete()
        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400


    @auth.verify_password
    def verify_password(username, password):
        user = models.Admin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True

class Connection(Resource):

    @auth.login_required
    def get(self, id=None):
        print('entering get')
        try:
            if not id:
                clients = models.Client.query.filter_by(user_id=g.user.id)
                data = [c.serialize() for c in clients]
                return data, 200
            else:
                permission = False
                for client in g.user.clients:
                    if client.id == id:
                        permission = True
                if not permission:
                    return 'You do not have access to this Client', 400
                return models.Client.query.get(id).get_token(), 200

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.verify_password
    def verify_password(username, password):
        user = models.User.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True

class User(Resource):

    @auth.login_required
    def get(self):
        try:
            users = models.User.query.filter_by(admin_id=g.user.id)
            return [u.serialize() for u in users], 200
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400

    @auth.login_required
    def put(self, id):
        data = request.get_json(force=True)
        try:
            client_ids = data['client_ids']
            clients = Client.query.filter(Client.id.in_(client_ids)).all()
            for client in clients:
                client.assign_user(id)
            return True, 200
        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.login_required
    def post(self):
        data = request.get_json(force=True)
        try:
            new_user = models.User(data['username'], data['password'], data['email'], g.user.id)
            if new_user.insert():
                return 'OK', 201
            return 'User Create Failed', 400
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400

    @auth.verify_password
    def verify_password(username, password):
        user = models.Admin.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True

class Blueprint(Resource):

    @auth.login_required
    def get(self):
        try:
            return g.user.get_blueprint(), 200
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400

    @auth.login_required
    def put(self):
        data = request.get_json(force=True)
        try:
            return g.user.set_blueprint_connection(data['rdp_uname'], data['rdp_pword']), 200
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400


    @auth.verify_password
    def verify_password(username, password):
        user = models.Admin.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True
