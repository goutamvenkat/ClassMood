from . import DBModels
import hashlib
import random
import datetime
from flask import session

class API(object):
    @staticmethod
    def get_student_class_list(student_id):
        members = DBModels.ClassMember.query.filter_by(student_id=student_id).all()
        result = []
        if members:
            for m in members:
                result.append(DBModels.Class.query.filter_by(id=m.class_id).first().name)
        return result

    @staticmethod
    def get_professor_class_list(professor_id):
        classes = DBModels.Class.query.filter_by(professor_id=professor_id).all()
        return [profClass.name for profClass in classes]

    @staticmethod
    def get_user_token(user_id):
        session = DBModels.Session.query.filter_by(user_id=user_id).first()
        if session:
            return session.token
        return None

    @staticmethod
    def create_prof_class(class_name, professor_id):
        existing_class = DBModels.Class.query.filter_by(professor_id=professor_id, name=class_name).first()
        if not existing_class:
            new_class = DBModels.Class(class_name, '', professor_id)
            DBModels.db.session.add(new_class)
            DBModels.db.session.commit()
            return True
        return False

    @staticmethod
    def set_student_class(class_name, student_id):
        requestedClass = DBModels.Class.query.filter_by(name=class_name).first()
        if requestedClass:
            student_existing_class = DBModels.ClassMember.query.filter_by(student_id=student_id,
                                                                          class_id=requestedClass.id).first()
            if not student_existing_class:
                new_class_membership = DBModels.ClassMember(student_id, requestedClass.id)
                DBModels.db.session.add(new_class_membership)
                DBModels.db.session.commit()
                return True
        return False

    @staticmethod
    def validate_login(email, user_password):
        user = DBModels.User.query.filter_by(email=email).first()
        if user:
            auth = DBModels.Authentication.query.filter_by(user_id=user.id).first()
            if auth:
                db_password, salt = auth.password.split(':')
                if user.email == email and db_password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest():
                    return user
        return None

    @staticmethod
    def get_authentication():
        if "token" in session:
            session_token = session["token"]
            sesh = DBModels.Session.query.filter_by(token=session_token).first()
            if sesh and abs(sesh.expires_at - datetime.datetime.now()) > datetime.timedelta(seconds=0):
                user = DBModels.User.query.filter_by(id=sesh.user_id).first()
                return user
        return None

    @staticmethod
    def get_access(typeid):
        return DBModels.UserType.query.filter_by(id=typeid).first()

    @staticmethod
    def create_session(userid):
        token = 0
        while token == 0:
            token = int(random.random() * 10 ** 10) #nonzero token
        newsesh = DBModels.Session(userid, token)
        oldsesh = DBModels.Session.query.filter_by(user_id=userid).first()
        if oldsesh:
            DBModels.db_rem(oldsesh)
        return token if DBModels.db_add(newsesh) else None

    @staticmethod
    def delete_session(session_token):
        sesh = DBModels.Session.query.filter_by(token=session_token).first()
        return DBModels.db_rem(sesh)
