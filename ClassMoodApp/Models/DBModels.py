import sys
import hashlib
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

db = SQLAlchemy()

class Providers(object):
    USERPASS = 'USERPASS'
    GOOGLE = 'GOOGLE'

class User(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(400), unique=True)
    is_student = Column(Boolean)
    def __init__(self, first_name, last_name, email, is_student):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_student = is_student

class Authentication(db.Model):
    __tablename__ = 'Authentication'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True, autoincrement=False)
    password = Column(String(sys.maxint))
    provider = Column(String(40))

    user_relation = relationship('User')
    def __init__(self, user_id, password, provider=Providers.USERPASS):
        self.user_id = user_id
        salt = uuid.uuid4().hex
        self.provider = provider
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

class Class(db.Model):
    __tablename__ = 'Classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    description = Column(String(400))
    professor_id = Column(Integer, ForeignKey('Users.id'))
    user_relation = relationship('User')
    live_lecture_id = Column(Integer, ForeignKey('LiveLectures.id', use_alter=True, name='fk_class_live_lecture_id'))
    live_lecture_relation = relationship('LiveLecture')
    def __init__(self, name, description, professor_id):
        self.name = name
        self.description = description
        self.professor_id = professor_id

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
    name = Column(String(40), nullable=False)
    class_id = Column(Integer, ForeignKey('Classes.id'))
    def __init__(self, name, class_id):
        self.name = name
        self.class_id = class_id

class LiveLecture(db.Model):
    __tablename__ = 'LiveLectures'
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('Lectures.id'))
    pace_total = Column(Float, nullable=False)
    depth_total = Column(Float, nullable=False)
    num_students = Column(Integer, nullable=False)
    def __init__(self, lecture_id):
        self.lecture_id = lecture_id
        self.pace_total = 0
        self.depth_total = 0
        self.num_students = 0

class Gauge(db.Model):
    __tablename__ = 'Gauges'
    id = Column(Integer, primary_key=True)
    live_lecture_id = Column(Integer, ForeignKey('LiveLectures.id'))
    student_id = Column(Integer, ForeignKey('Users.id'))
    depth = Column(Float, nullable=False)
    pace = Column(Float, nullable=False)
    def __init__(self, live_lecture_id, student_id):
        self.live_lecture_id = live_lecture_id
        self.student_id = student_id
        self.depth = 0
        self.pace = 0

class AnonymousQuestion(db.Model):
    __tablename__ = 'AnonymousQuestions'
    id = Column(Integer, primary_key=True)
    live_lecture_id = Column(Integer, ForeignKey('LiveLectures.id'))
    text = Column(String(1000), nullable=False)
    student_id = Column(Integer, ForeignKey('Users.id'))
    def __init__(self, live_lecture_id, text, student_id):
        self.live_lecture_id = live_lecture_id
        self.text = text
        self.student_id = student_id

class PollingQuestion(db.Model):
    __tablename__ = 'PollingQuestions'
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('Lectures.id'))
    text = Column(String(1000), nullable=False)
    a_text = Column(String(200))
    b_text = Column(String(200))
    c_text = Column(String(200))
    d_text = Column(String(200))
    answer = Column(String(1), nullable=False)
    def __init__(self, lecture_id, text, a_text, b_text, c_text, d_text, answer):
        self.lecture_id = lecture_id
        self.text = text
        self.a_text = a_text
        self.b_text = b_text
        self.c_text = c_text
        self.d_text = d_text
        self.answer = answer

class PollingQuestionResponse(db.Model):
    __tablename__ = 'PollingQuestionResponses'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    polling_question_id = Column(Integer, ForeignKey('PollingQuestions.id'), nullable=False)
    student_answer = Column(String(1), nullable=False)
    def __init__(self, student_id, polling_question_id, student_answer):
        self.student_id = student_id
        self.polling_question_id = polling_question_id
        self.student_answer = student_answer

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