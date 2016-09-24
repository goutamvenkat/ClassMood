from . import DBModels
from flask_sqlalchemy import SQLAlchemy
import hashlib
import random

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
    
    def is_login_valid(self, email, user_password):
        auth = DBModels.Authentication.query.filter_by(email=email).first()
        if auth:
            # password, salt = auth.password.split(':')
            # return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
            return auth.password == user_password #This is to make sure it works
        user = DBModels.User.query.filter_by(email=email).first()
        if user:
            auth = DBModels.Authentication.query.filter_by(user_id=user_id).first()
            if auth:
                password, salt = auth.password.split(':')
                return user.email == email and password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        return False

    def create_session(self, email):
        token = 0
        while token == 0:
            token = int(random.random() * 10 ** 10) #nonzero token
        newsesh = DBModels.UserSession(email, token)
        return token if DBModels.db_add(newsesh) else None

    def delete_session(self, session_token):
        sesh = DBModels.UserSession.query.filter_by(token=session_token).first()
        return DBModels.db_rem(sesh)

    
    
    