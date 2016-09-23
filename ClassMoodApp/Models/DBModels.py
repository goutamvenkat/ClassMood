from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
import sys
import hashlib
import uuid

db = SQLAlchemy()
student_type, professor_type = 'STUDENT', 'PROFESSOR'
class User(db.Model):
    email = db.Column(db.String(400), primary_key=True)
    user_type = db.Column(db.String(20), unique=True)
    def __init__(self, email, user_type):
        self.email = email
        self.user_type = user_type

class Authentication(db.Model):
    email = db.Column(db.String(400), primary_key=True)
    password = db.Column(db.String(sys.maxint))
    salt = uuid.uuid4().hex
    def __init__(self, email, password):
        self.email = email
        self.password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

class Student(db.Model):
    email = db.Column(db.String(400), primary_key=True)
    lectures = db.Column(PickleType())
    def __init__(self, email, lectures):
        self.email = email
        self.lectures = lectures

class Professor(db.Model):
    email = db.Column(db.String(400), primary_key=True)
    lectures = db.Column(PickleType())
    def __init__(self, email, lectures):
        self.email = email
        self.lectures = lectures

class Lecture(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    student_roster = db.Column(PickleType())
    lecturer = db.Column(db.String(400))
    def __init__(self, name, student_roster, lecturer):
        self.name = name
        self.student_roster = student_roster
        self.lecturer = lecturer

class UserSession(db.Model):
    email = db.Column(db.String(400), primary_key=True)
    token = db.Column(db.Integer())
    def __init__(self, email, token_id):
        self.email = email
        self.token = token_id

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