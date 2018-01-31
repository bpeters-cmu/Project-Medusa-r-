from flask import request, g, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug import secure_filename
from oci_api import OCIApi
from simplecrypt import encrypt
import logging
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
        logging.info('Registering new user')
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
            logging.debug('Exception: ', str(e))
            traceback.print_exc()
            return str(e), 400

    @auth.login_required
    def put(self):
        data = request.get_json(force=True)
        try:
            username = data['username']
            password = data['password']
            g.user.set_rdp(username, password)
            return 200
        except BaseException as e:
            print('Exception: ', str(e))
            traceback.print_exc()
            return str(e), 400


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
            print('getting instances')
            instances = g.user.get_instances(c_ocid)
            return instances, 200

        except BaseException as e:
            print('Exception: ', str(e))
            traceback.print_exc()
            return str(e), 400
    @auth.login_required
    def post(self, c_ocid=None):
        try:
            path = '/medusa_keys'
            print(request.form)
            f = request.files['file']
            data = request.form
            print('got file')
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join(path, secure_filename(data['ip']))
            self.encrypt_file(f, path, data['key'])
            return 200
        except BaseException as e:
            print('Exception: ', str(e))
            traceback.print_exc()
            return str(e), 400

    @auth.verify_password
    def verify_password(username, password):
        user = models.OCIAdmin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True
    def encrypt_file(self, f, path, key):
        data = f.read().decode("utf-8")
        encrypted = encrypt(key, data)
        f = open(path, 'wb')
        f.write(encrypted)
        f.close()

class Compartments(Resource):
    @auth.login_required
    def get(self):
        print('entering get')
        try:
            oci = OCIApi(g.user.user_ocid, g.user.key_path, g.user.fingerprint, g.user.tenancy_ocid, g.user.region)
            return oci.get_compartments(), 200
        except BaseException as e:
            print('Exception: ', str(e))
            traceback.print_exc()
            return str(e), 400

    @auth.verify_password
    def verify_password(username, password):
        user = models.OCIAdmin.query.filter_by(username = username).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
        print('User verified')
        g.user = user
        return True
