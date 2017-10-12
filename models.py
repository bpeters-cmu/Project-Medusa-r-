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
    ravello_password = db.Column(db.String(50))

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
        print('verifying password: ' + pword)
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

    def create_client(self, quantity):
        password = decrypt(config.key, self.ravello_password)
        ravello = Ravello(self.ravello_username, password)
        return ravello.create_applications(quantity)



class User(db.Model):
    __tablename__ = 'User'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column(db.String(25), unique=True , index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)

    def __init__(self, username, password, email, admin_id):
        self.username = username
        self.password = self.hash_password(password)
        self.hostname = hostname
        self.email = email
        self.admin_id = admin_id

    def hash_password(self, pword):
        hashed = phash.hash(pword)
        print(str(hashed))
        return hashed

    def verify_password(self, pword):
        print('verifying password: ' + pword)
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

    def get_token(self):
        json_data = {}
        json_data['connection']['type'] = self.conn_type
        json_data['connection']['settings']['hostname'] = self.hostname
        json_data['connection']['settings']['username'] = self.username
        json_data['connection']['settings']['password'] = self.password
        token = json.dumps(json_data).encode('utf-8')

        return base64.urlsafe_b64encode(token)

    def serialize(self):
        return {'username':self.username, 'email': self.email}


class Client(db.Model):
    __tablename__ = 'Client'
    id = db.Column('client_id',db.Integer , primary_key=True)
    conn_type = db.Column(db.String(3))
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.user_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    application_id = db.Column(db.Integer)
    name = db.Column(db.String(128))

    def __init__(self, admin_id, application_id, name):
        self.conn_type = 'rdp'
        self.admin_id = admin_id
        self.application_id = application_id
        self.name = name

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

    def serialize(self):
        return{}
