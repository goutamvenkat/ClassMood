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


    # return the lecture id of the lecture that is live for class_id
    @staticmethod
    def get_live_lecture(class_id):
        lecture = DBModels.Lecture.query.filter_by(class_id=class_id, is_live=True).first()
        if lecture:
            return lecture.id
        return None

    # disables the lecture that is live of class_id
    @staticmethod
    def disable_live_lecture(class_id):
        lecture = DBModels.Lecture.query.filter_by(class_id=class_id, is_live=True).first()
        if lecture:
            lecture.is_live = False
            return DBModels.db_update(lecture)
        return False

    # create a lecture that is live and returns the lecture id
    @staticmethod
    def create_live_lecture(class_id):
        new_lecture = DBModels.Lecture(class_id)
        new_lecture.is_live = True
        if DBModels.db_add(new_lecture):
            return new_lecture.id
        return None

    # add a student to the lecture
    @staticmethod
    def add_student_to_lecture(lecture_id):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            lecture.num_students += 1
            return DBModels.db_update(lecture)
        return False

    # get pace for a lecture
    @staticmethod
    def get_pace(lecture_id):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            return lecture.pace_total / lecture.num_students
        return None

    # get depth for a lecture
    @staticmethod
    def get_depth(lecture_id):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            return lecture.depth_total / lecture.num_students
        return None

    # change the total pace by num for lecture
    @staticmethod
    def change_total_pace_by(lecture_id, num):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            lecture.pace_total += num
            return DBModels.db_update(lecture)
        return False

    # change the total depth by num for lecture
    @staticmethod
    def change_total_depth_by(lecture_id, num):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            lecture.depth_total += num
            return DBModels.db_update(lecture)
        return False

    # return the current pace and depth for student in lecture
    @staticmethod
    def get_gauge_pace_and_depth(lecture_id, student_id):
        gauge = DBModels.Gauge.query.filter_by(lecture_id=lecture_id, student_id=student_id).first()
        if gauge:
            return (gauge.pace, gauge.depth)
        return None

    # add or update the current pace and depth for student in lecture
    @staticmethod
    def update_gauge_pace_and_depth(lecture_id, student_id, pace_num, depth_num):
        gauge = DBModels.Gauge.query.filter_by(lecture_id=lecture_id, student_id=student_id).first()
        if gauge:
            gauge.depth = depth_num
            gauge.pace = pace_num
            return DBModels.db_update(gauge)
        else:
            new_gauge = DBModels.Gauge(lecture_id, student_id)
            new_gauge.depth = depth_num
            new_gauge.pace = pace_num
            return DBModels.db_add(new_gauge)

    # return the question texts for a lecture
    @staticmethod
    def get_anonymous_questions(lecture_id):
        questions = DBModels.AnonymousQuestion.query.filter_by(lecture_id=lecture_id).all()
        if questions:
            return [q.text for q in questions]
        return []

    # add a question for a lecture
    @staticmethod
    def add_anonymous_question(lecture_id, student_id, text):
        question = DBModels.AnonymousQuestion(lecture_id, text, student_id)
        return DBModels.db_update(question)

