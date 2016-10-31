from . import DBModels
import hashlib
import random
import datetime
from flask import session

STUDENT = 'STUDENT'
PROFESSOR = 'PROFESSOR'
class API(object):
    @staticmethod
    def is_student(user_id):
        user = DBModels.User.query.filter_by(id=user_id).first()
        if user:
            return user.is_student
        return False

    @staticmethod
    def is_professor(user_id):
        user = DBModels.User.query.filter_by(id=user_id).first()
        if user:
            return ~user.is_student
        return False

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

    @staticmethod
    def get_class_id(class_name):
        class_obj = DBModels.Class.query.filter_by(name=class_name).first()
        return class_obj.id

    # return the live lecture id of the live lecture that is live for class_id
    @staticmethod
    def get_live_lecture(class_id):
        live_class = DBModels.Class.query.filter_by(id=class_id).first()
        if live_class and live_class.live_lecture_id:
            live_lecture = DBModels.LiveLecture.query.filter_by(id=live_class.live_lecture_id).first()
            if live_lecture:
                return live_lecture.id
        return None

    # disables the lecture that is live of class_id
    @staticmethod
    def disable_live_lecture(class_id):
        live_class = DBModels.Class.query.filter_by(id=class_id).first()
        if live_class:
            live_class.live_lecture_id = None
            return DBModels.db_update(live_class)
        return False

    # create a lecture with a given name
    @staticmethod
    def create_lecture(lecture_name, class_id):
        new_lecture = DBModels.Lecture(lecture_name, class_id)
        return DBModels.db_add(new_lecture)

    # create a lecture that is live and returns the live lecture id
    @staticmethod
    def create_live_lecture(lecture_id):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            lecture_class = DBModels.Class.query.filter_by(id=lecture.class_id).first()
            if lecture_class:
                new_live_lecture = DBModels.LiveLecture(lecture_id)
                if DBModels.db_add(new_live_lecture):
                    lecture_class.live_lecture_id = new_live_lecture.id
                    DBModels.db_update(lecture_class)
                    return new_live_lecture.id
        return None

    # add a student to the live lecture
    @staticmethod
    def add_student_to_live_lecture(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            live_lecture.num_students += 1
            return DBModels.db_update(live_lecture)
        return False

    # get pace for a live lecture
    @staticmethod
    def get_pace(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            return live_lecture.pace_total / live_lecture.num_students
        return None

    # get depth for a live lecture
    @staticmethod
    def get_depth(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            return live_lecture.depth_total / live_lecture.num_students
        return None

    # change the total pace by num for live lecture
    @staticmethod
    def change_total_pace_by(live_lecture_id, num):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            live_lecture.pace_total += num
            return DBModels.db_update(live_lecture)
        return False

    # change the total depth by num for live lecture
    @staticmethod
    def change_total_depth_by(live_lecture_id, num):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            live_lecture.depth_total += num
            return DBModels.db_update(live_lecture)
        return False

    # return the current pace and depth for student in live lecture
    @staticmethod
    def get_gauge_pace_and_depth(live_lecture_id, student_id):
        gauge = DBModels.Gauge.query.filter_by(live_lecture_id=live_lecture_id, student_id=student_id).first()
        if gauge:
            return (gauge.pace, gauge.depth)
        return None

    # add or update the current pace and depth for student in lecture
    @staticmethod
    def update_gauge_pace_and_depth(live_lecture_id, student_id, pace_num, depth_num):
        gauge = DBModels.Gauge.query.filter_by(live_lecture_id=live_lecture_id, student_id=student_id).first()
        if gauge:
            gauge.depth = depth_num
            gauge.pace = pace_num
            return DBModels.db_update(gauge)
        else:
            new_gauge = DBModels.Gauge(live_lecture_id, student_id)
            new_gauge.depth = depth_num
            new_gauge.pace = pace_num
            return DBModels.db_add(new_gauge)

    # return the question texts for a live lecture
    @staticmethod
    def get_anonymous_questions(live_lecture_id):
        questions = DBModels.AnonymousQuestion.query.filter_by(live_lecture_id=live_lecture_id).all()
        if questions:
            return [q.text for q in questions]
        return []

    # add a question for a lecture
    @staticmethod
    def add_anonymous_question(live_lecture_id, student_id, text):
        question = DBModels.AnonymousQuestion(live_lecture_id, text, student_id)
        return DBModels.db_update(question)

