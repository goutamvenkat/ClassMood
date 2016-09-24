from . import DBModels
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
import hashlib
<<<<<<< HEAD
import random

=======
>>>>>>> dev-goutam
class API(object):
    def get_student_class_list(self, email):
        student = DBModels.Student.query.filter_by(email=email).first()
        if student:
            return student.lectures
        return None

    def get_professor_class_list(self, email):
        professor = DBModels.Professor.query.filter_by(email=email).first()
        if professor:
            return professor.lectures
        return None
    
    def get_user_token(self, email):
        session = DBModels.UserSession.query.filter_by(email=email).first()
        if session:
            return session.token
        return None
    
    def is_login_valid(self, email, user_password):
        auth = DBModels.Authentication.query.filter_by(email=email).first()
        if auth:
            # password, salt = auth.password.split(':')
            # return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
            return auth.password == user_password #This is to make sure it works
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

