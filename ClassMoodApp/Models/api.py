from . import DBModels
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
import hashlib
class API(object):
    def get_student_class_list(self, email):
        student = DBModels.Student.query.filter_by(email=email).first()
        if student:
            return student.lectures
        return None

    def get_professor_class_list(self, email):
        professor = DBModels.Professor.query.filter_by(email=email).first()
        if professor:
            return professor.classes
        return None
    
    def get_user_token(self, email):
        session = DBModels.UserSession.query.filter_by(email=email).first()
        if session:
            return session.token
        return None
    
    def is_login_valid(self, email, user_password):
        auth = DBModels.Authentication.query.filter_by(email=email).first()
        if auth:
            password, salt = auth.password.split(':')
            return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        return False

    def create_class(self, class_name, professor_email):
        return True