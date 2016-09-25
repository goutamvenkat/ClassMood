from . import DBModels
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
import hashlib
import logging

class API(object):
    def get_student_lecture_list(self, student_id):
        roster = DBModels.Roster.query.filter_by(student_id=student_id).all()
        result = []
        if roster:
            for r in roster:
                result.append(DBModels.Lecture.query.filter_by(id=r.lecture_id).first().name)
        return result

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
            new_lecture = DBModels.Lecture(professor_id, '', lecture_name)
            DBModels.db.session.add(new_lecture)
            DBModels.db.session.commit()
            return True
        return False

    def set_student_lecture(self, lecture_name, student_id):
        lecture = DBModels.Lecture.query.filter_by(name=lecture_name).first()
        if lecture:
            student_existing_lecture = DBModels.Roster.query.filter_by(student_id=student_id, 
                                                                       lecture_id=lecture.id).first()
            if not student_existing_lecture:
                new_lecture = DBModels.Roster(student_id, lecture.id)
                DBModels.db.session.add(new_lecture)
                DBModels.db.session.commit()
                return True
        return False

    def is_login_valid(self, email, user_password):
        user = DBModels.User.query.filter_by(email=email).first()
        if user:
            auth = DBModels.Authentication.query.filter_by(user_id=user_id).first()
            if auth:
                db_password, salt = auth.password.split(':')
                return user.email == email and db_password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
        return False

