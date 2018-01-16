from flask import request, g, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug import secure_filename
import traceback
import models
import os

auth = HTTPBasicAuth()

class OCILogin(Resource):
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


class Admin(Resource):

    def post(self):
        print('register')
        data = request.form

        try:
            path = '/home/opc/.oci'
            f = request.files['file']
            print('got file')
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join(path, secure_filename(f.filename))
            f.save(path)
            print(path)
            new_user = models.OCIAdmin(data.get('username'), data.get('password'), data.get('user_ocid'), data.get('fingerprint'), data.get('tenancy_ocid'), data.get('region'), path)
            if new_user.insert():
                return 'OK', 201
            return 'User Create Failed', 400
        except BaseException as e:
            print('Exception: ', str(e))
            return str(e), 400

        @auth.login_required
        def put(self):
            data = request.get_json(force=True)
            try:
                g.user.set_rdp(data['username'], data['password'])
                return 200
            except BaseException as e:
                print('Exception: ', str(e))
                return 'Exception Occurred', 400


        @auth.verify_password
        def verify_password(username, password):
            user = models.OCIAdmin.query.filter_by(username = username).first()
            print(user)
            if not user or not user.verify_password(password):
                return False
            print('User verified')
            g.user = user
            return True

class Instances(Resource):
    @auth.login_required
    def get(self, c_ocid):
        print('entering get')
        try:
            instances = g.user.get_instances(c_ocid)
            return flask.jsonify(instances), 200

        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.verify_password
    def verify_password(username, password):
        user = models.OCIAdmin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True

class Compartments(Resource):
    @auth.login_required
    def get(self):
        print('entering get')
        try:
            compartments = g.user.compartments
            if compartments:
                return [c.serialize() for c in compartments], 200
            return None, 200
        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.login_required
    def post(self):
        try:
            data = request.get_json(force=True)
            g.user.add_compartment(data['name'], data['compartment_ocid'])
            return 200
        except BaseException as e:
            print('Exception: ', str(e))
            return 'Exception Occurred', 400

    @auth.verify_password
    def verify_password(username, password):
        user = models.OCIAdmin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True
