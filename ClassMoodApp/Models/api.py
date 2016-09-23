from . import DBModels
from flask_sqlalchemy import SQLAlchemy
import hashlib
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
        user = DBModels.User.query.filter_by(email=email).first()
        if user:
            auth = DBModels.Authentication.query.filter_by(user_id=user_id).first()
            if auth:
                password, salt = auth.password.split(':')
                return user.email == email and password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        return False

