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
        apps = ravello.create_applications(quantity)
        if not apps:
            return None
        clients = []
        for app in apps:
            client = new Client(self.id, app[0], app[1], app[2])
            clients.append(client)
        return self.insert_clients(clients)

    def insert_clients(self, clients):
        try:
            db.session.add(clients)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False

    def get_blueprint(self):
        ravello = Ravello(self.ravello_username, self.ravello_password)
        bp_id, description = ravello.get_gold_image()
        if not self.blueprint:
            bp = Blueprint(self.id, bp_id, description)
            bp.insert()
            return bp.serialize()
        if self.blueprint[0].bp_id == bp_id:
            return self.blueprint[0].serialize()
        else:
            db.session.delete(self.blureprint[0])
            db.session.commit()
            bp = Blueprint(self.id, bp_id, description)
            bp.insert()
            return bp.serialize()

            
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
        return {'username':self.username, 'email': self.email, 'clients':clients}


class Client(db.Model):
    __tablename__ = 'Client'
    id = db.Column('client_id',db.Integer , primary_key=True)
    conn_type = db.Column(db.String(3))
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    application_id = db.Column(db.Integer)
    vm_id = db.Column(db.Integer)
    name = db.Column(db.String(128))

    def __init__(self, admin_id, application_id, name, vm_id):
        self.conn_type = 'rdp'
        self.admin_id = admin_id
        self.application_id = application_id
        self.name = name
        self.vm_id = vm_id

    def assign_user(self, user_id):
        self.user_id = user_id
        db.session.commit()

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

    def get_token(self, ravello):
        json_data = {}
        json_data['connection']['type'] = self.conn_type
        json_data['connection']['settings']['hostname'] = ravello.get_ip(self.application_id, self.vm_id)
        json_data['connection']['settings']['username'] = ''
        json_data['connection']['settings']['password'] = ''
        token = json.dumps(json_data).encode('utf-8')

        return base64.urlsafe_b64encode(token)

    def serialize(self, ravello):
        username = self.user.username
        ip = ravello.get_ip(self.application_id, self.vm_id)
        return{'name':self.name, 'application_id':self.application_id, 'assigned_user': username, 'ip':ip }

class Blueprint(db.Model):
    __tablename__ = 'Blueprint'
    id = db.Column('blueprint_id',db.Integer , primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)
    description = db.Column(db.String(128))
    bp_id = db.Column(db.Integer)

    def __init__(self, admin_id, bp_id, description):
        self.admin_id = admin_id
        self.blueprint_id = bp_id
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
        return {'description': self.description}
