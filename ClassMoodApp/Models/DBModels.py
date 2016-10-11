import sys
import hashlib
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

db = SQLAlchemy()

class UserType(db.Model):
    __tablename__ = 'UserTypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(400))
    can_add_class = Column(Boolean())
    can_list_classes = Column(Boolean())
    def __init__(self, name, can_add_class, can_list_classes):
        self.name = name
        self.can_add_class = can_add_class
        self.can_list_classes = can_list_classes

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(400), unique=True)
    user_type = Column(Integer, ForeignKey('UserTypes.id'))
    user_type_rel = relationship('UserType')
    def __init__(self, first_name, last_name, email, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type

class Class(db.Model):
    __tablename__ = 'Classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    description = Column(String(400))
    professor_id = Column(Integer, ForeignKey('Users.id'))
    user_relation = relationship('User')
    def __init__(self, name, description, professor_id):
        self.name = name
        self.description = description
        self.professor_id = professor_id

class Authentication(db.Model):
    __tablename__ = 'Authentication'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    password = Column(String(sys.maxint))
    user_relation = relationship('User')
    def __init__(self, user_id, password):
        self.user_id = user_id
        salt = uuid.uuid4().hex
        self.password = '{}:{}'.format(hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt)

class Session(db.Model):
    __tablename__ = 'Sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), unique=True)
    token = Column(BigInteger())
    created_at = Column(DateTime())
    expires_at = Column(DateTime())
    user_relation = relationship('User')
    def __init__(self, user_id, token):
        self.token = token
        self.user_id = user_id
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(hours=2)
    def __repr__(self):
        return "token:{}, id:{}, userid:{}, create:{}, expire:{}".format(str(self.token), str(self.id), str(self.user_id), str(self.created_at), str(self.expires_at))

class ClassMember(db.Model):
    __tablename__ = 'ClassMembers'
    student_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('Classes.id'), primary_key=True)
    user_relation = relationship('User')
    lecture_relation = relationship('Class')
    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

class Lecture(db.Model):
    __tablename__ = 'Lectures'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('Classes.id'))
    is_live = Column(Boolean, nullable=False)
    pace_total = Column(Float, nullable=False)
    depth_total = Column(Float, nullable=False)
    num_students = Column(Integer, nullable=False)
    def __init__(self, class_id):
        self.class_id = class_id
        self.is_live = False
        self.pace_total = 0
        self.depth_total = 0
        self.num_students = 0

class Gauge(db.Model):
    __tablename__ = 'Gauges'
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('Lectures.id'))
    depth = Column(Float, nullable=False)
    pace = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey('Users.id'))
    def __init__(self, lecture_id, student_id):
        self.lecture_id = lecture_id
        self.depth = 0
        self.pace = 0
        self.student_id = student_id

class AnonymousQuestion(db.Model):
    __tablename__ = 'AnonymousQuestions'
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('Lectures.id'))
    text = Column(String(1000), nullable=False)
    student_id = Column(Integer, ForeignKey('Users.id'))
    def __init__(self, lecture_id, text, student_id):
        self.lecture_id = lecture_id
        self.text = text
        self.student_id = student_id

def db_add(*obj):
    if obj:
        for entry in obj:
            db.session.add(entry)
        db.session.commit()
        return True
    return False

def db_rem(*obj):
    if obj:
        for entry in obj:
            db.session.delete(entry)
        db.session.commit()
        return True
    return False

def db_update(*obj):
    if obj:
        for entry in obj:
            db.session.merge(entry)
        db.session.commit()
        return True
    return False