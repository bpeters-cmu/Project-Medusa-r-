from passlib.hash import pbkdf2_sha256 as phash
from app import db
from simplecrypt import encrypt, decrypt
from ravello import Ravello
import os
import json
import base64
import config



class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column(db.String(25), unique=True , index=True)
    password = db.Column(db.String(128))
    ravello_username = db.Column(db.String(35))
    ravello_password = db.Column(db.BLOB())
    users = db.relationship('User', backref=db.backref('admin', lazy=True))
    clients = db.relationship('Client', backref=db.backref('admin', lazy=True))
    blueprint = db.relationship('Blueprint', backref=db.backref('admin', lazy=True))

    def __init__(self, username, password, ravello_username, ravello_password):
        self.username = username
        self.password = self.hash_password(password)
        self.ravello_username = ravello_username
        self.ravello_password = encrypt(config.key, ravello_password)

    def hash_password(self, pword):
        hashed = phash.hash(pword)
        print(str(hashed))
        return hashed

    def verify_password(self, pword):
        print(phash.verify(pword, self.password))
        return phash.verify(pword, self.password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False

    def __str__(self):
        return self.username + ' ' + self.password

    def create_user(self, client_username, client_password, hostname):
        user = User(client_username, client_password, hostname, self.id)
        user.insert()

    def create_clients(self, quantity):
        password = decrypt(config.key, self.ravello_password)
        ravello = Ravello(self.ravello_username, password)
        apps = ravello.create_applications(quantity, bp_id=self.blueprint[0].bp_id)
        if not apps:
            return None

        for app in apps:
            client = Client(self.id, str(app[0]), app[1], str(app[2]), self.blueprint[0].id)
            print(self.blueprint[0].id)
            print(client.bp_id)
            self.insert_client(client)

    def insert_client(self, client):
        try:
            db.session.add(client)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False

    def get_blueprint(self):
        print('getting blueprint')
        password = decrypt(config.key, self.ravello_password)
        ravello = Ravello(self.ravello_username, password)
        bp_id, description = ravello.get_gold_image()
        print(bp_id, description)
        if not self.blueprint:
            bp = Blueprint(self.id, str(bp_id), description)
            print(bp.serialize())
            bp.insert()
            return bp.serialize()
        if self.blueprint[0].bp_id == bp_id:
            print('2')
            return self.blueprint[0].serialize()
        else:
            print('3')
            db.session.delete(self.blueprint[0])
            db.session.commit()
            bp = Blueprint(self.id, bp_id, description)
            bp.insert()
            return bp.serialize()

    def set_blueprint_connection(self, rdp_uname, rdp_pword):
        self.blueprint[0].rdp_uname = rdp_uname
        self.blueprint[0].rdp_pword = encrypt(config.key, rdp_pword)
        db.session.commit()
        return True


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column(db.String(25), unique=True , index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)
    clients = db.relationship('Client', backref=db.backref('user', lazy=True))

    def __init__(self, username, password, email, admin_id):
        self.username = username
        self.password = self.hash_password(password)
        self.email = email
        self.admin_id = admin_id

    def hash_password(self, pword):
        hashed = phash.hash(pword)
        print(str(hashed))
        return hashed

    def verify_password(self, pword):
        print(phash.verify(pword, self.password))
        return phash.verify(pword, self.password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False


    def serialize(self):
        clients = [c.serialize() for c in self.clients]
        return {'id': self.id, 'username':self.username, 'email': self.email, 'clients':clients}


class Client(db.Model):
    __tablename__ = 'Client'
    id = db.Column('client_id',db.Integer , primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=True)
    application_id = db.Column(db.String(128))
    vm_id = db.Column(db.String(128))
    name = db.Column(db.String(128))
    bp_id = db.Column(db.Integer, db.ForeignKey('Blueprint.blueprint_id'))

    def __init__(self, admin_id, application_id, name, vm_id, bp_id):
        self.admin_id = admin_id
        self.application_id = application_id
        self.name = name
        self.vm_id = vm_id
        self.bp_id = bp_id

    def assign_user(self, user_id):
        self.user_id = user_id
        db.session.commit()
        return True

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False

    def get_token(self):
        if not self.rdp_uname or not self.rdp_pword:
            return None

        password = decrypt(config.key, self.admin.ravello_password)
        ravello = Ravello(self.admin.ravello_username, password)
        print(self.blueprint)
        print(self.blueprint.rdp_uname)

        json_data = {}
        json_data['connection'] = {}
        json_data['connection']['settings'] = {}
        json_data['connection']['type'] = 'rdp'
        json_data['connection']['settings']['hostname'] = ravello.get_ip(self.application_id, self.vm_id)
        json_data['connection']['settings']['username'] = self.blueprint.rdp_uname
        json_data['connection']['settings']['password'] = decrypt(config.key, self.blueprint.rdp_pword)
        token = json.dumps(json_data).encode('utf-8')

        return {'token': base64.urlsafe_b64encode(token)}

    def serialize(self):
        password = decrypt(config.key, self.admin.ravello_password)
        ravello = Ravello(self.admin.ravello_username, password)
        username = 'None'
        if self.user:
            username = self.user.username
        status = ravello.get_vm_state(self.application_id, self.vm_id)
        return{'name':self.name, 'id':self.id, 'assigned_user': username, 'status':status }

    def start_stop(self, action):
        password = decrypt(config.key, self.admin.ravello_password)
        ravello = Ravello(self.admin.ravello_username, password)
        if action == 'start':
            return ravello.start_app(self.application_id)
        elif action == 'stop':
            return ravello.stop_app(self.application_id)
        else:
            raise Exception('Action must be start or stop')

class Blueprint(db.Model):
    __tablename__ = 'Blueprint'
    id = db.Column('blueprint_id',db.Integer , primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)
    description = db.Column(db.String(128))
    bp_id = db.Column(db.String(128))
    clients = db.relationship('Client', backref=db.backref('blueprint', lazy=True))
    rdp_uname = db.Column(db.String(50))
    rdp_pword = db.Column(db.String(50))

    def __init__(self, admin_id, bp_id, description):
        self.admin_id = admin_id
        self.bp_id = bp_id
        self.description = description

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False

    def serialize(self):
        credentials = False
        if self.rdp_uname and self.rdp_pword:
            credentials = True
        return {'description': self.description, 'credentials': credentials}
