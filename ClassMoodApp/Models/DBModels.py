from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
import sys
import hashlib
import uuid
from datetime import datetime, timedelta

db = SQLAlchemy()
student_type, professor_type = 'STUDENT', 'PROFESSOR'

class UserType(db.Model):
    __tablename__ = 'UserType'
    id = db.Column(db.BigInteger(), db.ForeignKey('User.user_type'), primary_key=True)
    name = db.Column(db.String(400))
    can_add_class = db.Column(db.Boolean())
    can_list_classes = db.Column(db.Boolean())
    user_relationship = db.relationship('User')
    def __init__(self, name, can_add_class, can_list_classes):
        self.id = uuid.uuid4().int
        self.name = name
        self.can_add_class = can_add_class
        self.can_list_classes = can_list_classes

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.BigInteger(), 
                    db.ForeignKey('Lecture.professor_id'), 
                    db.ForeignKey('Sessions.user_id'), 
                    db.ForeignKey('Authentication.user_id'),
                    db.ForeignKey('Roster.student_id'),
                    primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(400), unique=True)
    user_type = db.Column(db.BigInteger())
    professor = db.relationship('Lecture')
    sessions = db.relationship('Sessions')
    auth = db.relationship('Authentication')

    def __init__(self, first_name, last_name, email, user_type):
        self.id = uuid.uuid4().int
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type

class Lecture(db.Model):
    __tablename__ = 'Lecture'
    id = db.Column(db.BigInteger(), db.ForeignKey('Roster.lecture_id'), primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(400))
    professor_id = db.Column(db.BigInteger())
    def __init__(self, name, description, professor_id):
        self.id = uuid.uuid4().int
        self.name = name
        self.professor_id = professor_id

class Authentication(db.Model):
    __tablename__ = 'Authentication'
    user_id = db.Column(db.BigInteger(), primary_key=True)
    password = db.Column(db.String(sys.maxint))
    salt = uuid.uuid4().hex
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = '{}:{}'.format(hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt)

class Sessions(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.BigInteger(), unique=True)
    token = db.Column(db.BigInteger())
    created_at = db.Column(db.DateTime())
    expires_at = db.Column(db.DateTime())
    def __init__(self, user_id, token):
        self.token = token
        self.id = uuid.uuid4().int
        self.user_id = user_id
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(hours=2)

class Roster(db.Model):
    __tablename__ = 'Roster'
    student_id = db.Column(db.BigInteger(), primary_key=True)
    lecture_id = db.Column(db.BigInteger(), primary_key=True)
    def __init__(self, student_id, lecture_id):
        self.student_id = student_id
        self.lecture_id = lecture_id
    
