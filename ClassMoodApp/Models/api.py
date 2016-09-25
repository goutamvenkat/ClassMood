from . import DBModels
from flask_sqlalchemy import SQLAlchemy
import hashlib
import random
import datetime
from sqlalchemy import PickleType
from flask import session

class API(object):
    def get_student_class_list(self, student_id):
        roster = DBModels.Roster.query.filter_by(student_id=student_id).all()
        if roster:
            return [lecture_id for lecture_id in roster.lecture_id]
        return None

    def get_professor_class_list(self, professor_id):
        lectures = DBModels.Lecture.query.filter_by(professor_id=professor_id).all()
        return lectures
    
    def get_user_token(self, user_id):
        session = DBModels.Sessions.query.filter_by(user_id=user_id).first()
        if session:
            return session.token
        return None
    
    def create_prof_lecture(self, lecture_name, professor_id):
        existing_lecture = DBModels.Lecture.query.filter_by(professor_id=professor_id, name=lecture_name).first()
        if not existing_lecture:
            new_lecture = DBModels.Lecture(professor_id=professor_id, name=lecture_name)
            db.session.add(new_lecture)
            db.session.commit()
            return True
        return False

    def set_student_lecture(self, lecture_name, student_id):
        lecture_id = DBModels.Lecture.query.filter_by(name=lecture_name).first().id
        student_existing_lecture = DBModels.Roster.query.filter_by(student_id=student_id, 
                                                                   lecture_id=lecture_id).first()
        if not student_existing_lecture:
            new_lecture = DBModels.Roster(student_id=student_id, lecture_id=lecture_id)
            db.session.add(new_lecture)
            db.session.commit()
            return True
        return False

    def is_login_valid(self, email, user_password):
        user = DBModels.User.query.filter_by(email=email).first()
        if user:
            auth = DBModels.Authentication.query.filter_by(user_id=user.id).first()
            if auth:
                password, salt = auth.password.split(':')
                return user.email == email and password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        return False

    def is_authenticated(self):
        session_token = session["token"]
        sesh = DBModels.Sessions.query.filter_by(token=session_token).first()
        if sesh and abs(sesh.expires_at - datetime.now()) > timedelta(seconds=0):
            return True
        return False

    def create_session(self, email):
        token = 0
        while token == 0:
            token = int(random.random() * 10 ** 10) #nonzero token
        newsesh = DBModels.Sessions(email, token)
        return token if DBModels.db_add(newsesh) else None

    def delete_session(self, session_token):
        sesh = DBModels.Sessions.query.filter_by(token=session_token).first()
        return DBModels.db_rem(sesh)


