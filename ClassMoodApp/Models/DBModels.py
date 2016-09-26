from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
import sys
import hashlib
import uuid
from datetime import datetime, timedelta

db = SQLAlchemy()
student_type, professor_type = 'STUDENT', 'PROFESSOR'

class UserType(db.Model):
    __tablename__ = 'UserTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    can_add_class = db.Column(db.Boolean())
    can_list_classes = db.Column(db.Boolean())
    def __init__(self, name, can_add_class, can_list_classes):
        self.name = name
        self.can_add_class = can_add_class
        self.can_list_classes = can_list_classes

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(400), unique=True)
    user_type = db.Column(db.Integer, db.ForeignKey('UserTypes.id'))
    user_type_rel = db.relationship('UserType')
    def __init__(self, first_name, last_name, email, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type

class Class(db.Model):
    __tablename__ = 'Classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(400))
    professor_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user_relation = db.relationship('User')
    def __init__(self, name, description, professor_id):
        self.name = name
        self.description = description
        self.professor_id = professor_id

class Authentication(db.Model):
    __tablename__ = 'Authentication'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    password = db.Column(db.String(sys.maxint))
    user_relation = db.relationship('User')
    def __init__(self, user_id, password):
        self.user_id = user_id
        salt = uuid.uuid4().hex
        self.password = '{}:{}'.format(hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt)

class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), unique=True)
    token = db.Column(db.BigInteger())
    created_at = db.Column(db.DateTime())
    expires_at = db.Column(db.DateTime())
    user_relation = db.relationship('User')
    def __init__(self, user_id, token):
        self.token = token
        self.user_id = user_id
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(hours=2)
    def __repr__(self):
        return "token:{}, id:{}, userid:{}, create:{}, expire:{}".format(str(self.token), str(self.id), str(self.user_id), str(self.created_at), str(self.expires_at))

class ClassMember(db.Model):
    __tablename__ = 'ClassMembers'
    student_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.id'), primary_key=True)
    user_relation = db.relationship('User')
    lecture_relation = db.relationship('Class')
    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

def db_add(obj):
    if obj:
        db.session.add(obj)
        db.session.commit()
        return True
    return False

def db_rem(obj):
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return True
    return False

