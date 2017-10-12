from flask import request, g
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
import traceback
import app_service
import models

auth = HTTPBasicAuth()

class Register(Resource):

    def post(self):
        data = request.get_json(force=True)
        try:
            new_user = models.Admin(data['username'], data['password'], data['tenancy_ocid'],
            data['user_ocid'], data['fingerprint'], data['private_key'], data['region'])
            if new_user.insert():
                return 'OK',200
            return 'User Create Failed', 400
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400


class VdiClient(Resource):

    @auth.login_required
    def get(self):
        print('enter get')
        try:
            return app_service.get_instances(g.user),200

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.login_required
    def post(self):
        data = request.get_json(force=True)
        try:
            return g.user.create_client(data['quantity']), 200

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400



    @auth.verify_password
    def verify_password(username, password):
        print('user:' + username + 'end')
        print('password: ' + password)
        user = models.Admin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True

class Connection(Resource):

    @auth.login_required
    def get(self):
        print('enter get')
        try:
            return g.user.get_token()

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.verify_password
    def verify_password(username, password):
        print('user:' + username + 'end')
        print('password: ' + password)
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


        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400

    @auth.login_required
    def post(self):
        data = request.get_json(force=True)
        try:
            new_user = models.User(data['username'], data['password'], data['email'], g.user.id)
            if new_user.insert():
                return 'OK',200
            return 'User Create Failed', 400
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400


    @auth.verify_password
    def verify_password(username, password):
        print('user:' + username + 'end')
        print('password: ' + password)
        user = models.Admin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True
