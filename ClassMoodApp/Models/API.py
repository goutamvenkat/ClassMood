from . import DBModels
import hashlib
import random
import datetime
from flask import session, request
from collections import defaultdict
from sqlalchemy import desc

STUDENT = 'STUDENT'
PROFESSOR = 'PROFESSOR'
class API(object):

    # Checks if the current user is a student
    @staticmethod
    def is_student(user_id):
        user = DBModels.User.query.filter_by(id=user_id).first()
        if user:
            return user.is_student
        return False

    # Checks if the current user is a professor
    @staticmethod
    def is_professor(user_id):
        user = DBModels.User.query.filter_by(id=user_id).first()
        if user:
            return not user.is_student
        return False

    # Gets the student class list
    @staticmethod
    def get_student_class_list(student_id):
        members = DBModels.ClassMember.query.filter_by(student_id=student_id).all()
        result = []
        if members:
            for m in members:
                result.append(DBModels.Class.query.filter_by(id=m.class_id).first().name)
        return result

    # Gets the professor class list
    @staticmethod
    def get_professor_class_list(professor_id):
        classes = DBModels.Class.query.filter_by(professor_id=professor_id).all()
        return [profClass.name for profClass in classes]

    # Gets the token for a given user id
    @staticmethod
    def get_user_token(user_id):
        session = DBModels.Session.query.filter_by(user_id=user_id).first()
        if session:
            return session.token
        return None

    # Creates a class for a professor
    @staticmethod
    def create_prof_class(class_name, professor_id):
        existing_class = DBModels.Class.query.filter_by(professor_id=professor_id, name=class_name).first()
        if not existing_class:
            new_class = DBModels.Class(class_name, '', professor_id)
            DBModels.db.session.add(new_class)
            DBModels.db.session.commit()
            return True
        return False

    # Adds a student to a class
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

    # Validates a login request given an email and password
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

    # Checks if the current user is authenticated
    @staticmethod
    def get_authentication(session_token=None):
        # if "token" in session:
        #     session_token = session["token"]
        if not session_token:
            session_token = request.cookies.get('token')
        sesh = DBModels.Session.query.filter_by(token=session_token).first()
        if sesh and abs(sesh.expires_at - datetime.datetime.now()) > datetime.timedelta(seconds=0):
            user = DBModels.User.query.filter_by(id=sesh.user_id).first()
            return user
        return None

    # Checks if the current account is a Google account
    @staticmethod
    def is_google_account():
        user = API.get_authentication()
        if user:
            auth = DBModels.Authentication.query.filter_by(user_id=user.id).first()
            return auth and auth.provider == DBModels.Providers.GOOGLE
        return False

    # Gets the Google user given an email and name
    @staticmethod
    def get_google_user(email, name):
        existing_google_user = DBModels.User.query.filter_by(email=email).first()
        if not existing_google_user:
            fname, lname = name.split()
            new_google_user = DBModels.User(fname, lname, email, True)
            DBModels.db_add(new_google_user)
            new_auth = DBModels.Authentication(new_google_user.id, 'blah:blah', DBModels.Providers.GOOGLE)
            DBModels.db_add(new_auth)
            # API.create_session(new_google_user.id)
            return new_google_user
        # API.create_session(existing_google_user.id)
        return existing_google_user

    # Creates a session for a given user
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

    # Deletes a session given a session token
    @staticmethod
    def delete_session(session_token):
        sesh = DBModels.Session.query.filter_by(token=session_token).first()
        return DBModels.db_rem(sesh)

    # Gets the class id for a given class name
    @staticmethod
    def get_class_id(class_name):
        class_obj = DBModels.Class.query.filter_by(name=class_name).first()
        return class_obj.id

    # Return the live lecture id of the lecture that is live for class_id
    @staticmethod
    def get_live_lecture(class_id):
        live_class = DBModels.Class.query.filter_by(id=class_id).first()
        if live_class and live_class.live_lecture_id:
            live_lecture = DBModels.LiveLecture.query.filter_by(id=live_class.live_lecture_id).first()
            if live_lecture:
                return live_lecture.id
        return None

    # Returns the lecture associated with a live lecture
    @staticmethod
    def get_lecture_from_live_lecture(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            lecture = DBModels.Lecture.query.filter_by(id=live_lecture.lecture_id).first()
            if lecture:
                return lecture.id
        return None

    # Returns the title of a given lecture
    @staticmethod
    def get_lecture_title(lecture_id):
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture is not None:
            return lecture.name
        return "Live Lecture"

    # Disables the lecture that is live of class_id
    @staticmethod
    def disable_live_lecture(class_id):
        live_class = DBModels.Class.query.filter_by(id=class_id).first()
        if live_class:
            live_class.live_lecture_id = None
            return DBModels.db_update(live_class)
        return False

    # Creates a lecture with a given name
    @staticmethod
    def create_lecture(lecture_name, class_id):
        new_lecture = DBModels.Lecture(lecture_name, class_id)
        return DBModels.db_add(new_lecture)

    # Creates a lecture that is live and returns the live lecture id
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
                    return lecture_class.id
        return None

    # Gets the current live lecture's polling question
    @staticmethod
    def get_current_polling_question(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            qid = live_lecture.current_polling_qid
            q = DBModels.PollingQuestion.query.filter_by(id=qid).first()
            if q:
                return dict(id=q.id, text=q.text, a_text=q.a_text, b_text=q.b_text, c_text=q.c_text, d_text=q.d_text)
        return None

    # Returns success based on whether the live lecture's current qid was updated
    @staticmethod
    def present_polling_question(live_lecture_id, polling_qid):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            q = DBModels.PollingQuestion.query.filter_by(id=polling_qid).first()
            if q:
                live_lecture.current_polling_qid = polling_qid
                DBModels.db_update(live_lecture)
                return True
        return False
    
    # Adds a student's reponse to a polling question
    @staticmethod
    def respond_to_polling_question(student_id, polling_qid, student_ans):
        if student_id and polling_qid and student_ans:
            response = DBModels.PollingQuestionResponse.query.filter_by(student_id=student_id, polling_question_id=polling_qid).first()
            if response:
                response.student_answer = student_ans
                DBModels.db_update(response)
            else:
                new_response = DBModels.PollingQuestionResponse(student_id, polling_qid, student_ans)
                DBModels.db_add(new_response)
            return True
        return False

    # Stops the current polling question for a live lecture
    @staticmethod
    def stop_polling_questions(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            lecture_id = live_lecture.lecture_id
            polling_qs= DBModels.PollingQuestion.query.filter_by(lecture_id=lecture_id).all()
            responses_dict = defaultdict(dict)
            for q in polling_qs:
                student_responses = DBModels.PollingQuestionResponse.query.filter_by(polling_question_id=q.id).all()
                correct_answer = DBModels.PollingQuestion.query.filter_by(id=q.id).first().answer
                q_response_dict = defaultdict(float)
                for response in student_responses:
                    q_response_dict[response.student_answer] += (1.0/len(student_responses))*100
                responses_dict[q.id] = q_response_dict
                responses_dict[q.id]['correct_answer'] = correct_answer
                responses_dict[q.id]['num_responses'] = len(student_responses)
            live_lecture.current_polling_qid = None
            DBModels.db_update(live_lecture)
            return responses_dict
        return None

    # Adds a student to the live lecture
    @staticmethod
    def add_student_to_live_lecture(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            live_lecture.num_students += 1
            if DBModels.db_update(live_lecture):
                live_class = DBModels.Class.query.filter_by(live_lecture_id=live_lecture_id).first()
                if live_class is not None:
                    return live_class.id
        return -1

    # Gets the pace for a live lecture
    @staticmethod
    def get_pace(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            if live_lecture.num_students > 0:
                return live_lecture.pace_total / live_lecture.num_students
            else:
                return 0
        return None

    # Gets the depth for a live lecture
    @staticmethod
    def get_depth(live_lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            if live_lecture.num_students > 0:
                return live_lecture.depth_total / live_lecture.num_students
            else:
                return 0
        return None

    # Change the total pace by num for a live lecture
    @staticmethod
    def change_total_pace_by(live_lecture_id, num):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            live_lecture.pace_total += num
            return DBModels.db_update(live_lecture)
        return False

    # Changes the total depth by num for a live lecture
    @staticmethod
    def change_total_depth_by(live_lecture_id, num):
        live_lecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        if live_lecture:
            live_lecture.depth_total += num
            return DBModels.db_update(live_lecture)
        return False

    # Returns the current pace and depth for a student in a live lecture
    @staticmethod
    def get_gauge_pace_and_depth(live_lecture_id, student_id):
        gauge = DBModels.Gauge.query.filter_by(live_lecture_id=live_lecture_id, student_id=student_id).first()
        if gauge:
            return (gauge.pace, gauge.depth)
        return None

    # Adds or updates the current pace and depth for a student in a lecture
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

    # Returns the question texts for a live lecture
    @staticmethod
    def get_anonymous_questions(live_lecture_id):
        questions = DBModels.AnonymousQuestion.query.filter_by(live_lecture_id=live_lecture_id).all()
        if questions:
            return [q.text for q in questions]
        return []

    # Adds a question to a lecture
    @staticmethod
    def add_anonymous_question(live_lecture_id, student_id, text):
        question = DBModels.AnonymousQuestion(live_lecture_id, text, student_id)
        return DBModels.db_update(question)


    # Lists all the lectures in a class
    @staticmethod
    def get_lecture_list(class_id):
        lectures = DBModels.Lecture.query.filter_by(class_id=class_id).order_by(desc(DBModels.Lecture.creation_time)).all()
        ret = []
        if lectures:
            for l in lectures:
                questions = DBModels.PollingQuestion.query.filter_by(lecture_id=l.id).all()
                ret.append({"lecture_id" : l.id, "lecture_name" : l.name, "num_questions" : len(questions), "creation_time" : l.creation_time})
        return ret

    # Create a new polling question
    @staticmethod
    def create_polling_question(lecture_id, q_text, a_text, b_text, c_text, d_text, ans):
        question = DBModels.PollingQuestion(lecture_id, q_text, a_text, b_text, c_text, d_text, ans)
        return DBModels.db_add(question)

    # Lists all polling questions for a lecture
    @staticmethod
    def get_polling_questions(lecture_id):
        questions = DBModels.PollingQuestion.query.filter_by(lecture_id=lecture_id).all()
        questionInformation = []
        if questions:
            for q in questions:
                questionInformation.append(dict(id=q.id, text=q.text, a_text=q.a_text, b_text=q.b_text, c_text=q.c_text, d_text=q.d_text, answer=q.answer))
        return questionInformation

    

    # Delete a single polling question and the reponses assoicated with the polling question
    @staticmethod
    def delete_polling_question(polling_question_id):
        question = DBModels.PollingQuestion.query.filter_by(id=polling_question_id).first()
        if question:
            DBModels.db_rem(question)
        responses = DBModels.PollingQuestionResponse.query.filter_by(polling_question_id=polling_question_id).all()
        if responses:
            for r in responses:
                DBModels.db_rem(r)
        return True

    # Delete a single lecture, polling questions, polling question responses, live lecture, gauges, and anonymous questions assoicated with the lecture
    @staticmethod
    def delete_lecture(lecture_id):
        live_lecture = DBModels.LiveLecture.query.filter_by(lecture_id=lecture_id).first()
        if live_lecture:
            DBModels.db_rem(live_lecture)
            gauges = DBModels.Gauge.query.filter_by(live_lecture_id=live_lecture.id).all()
            if gauges:
                for g in gauges:
                    DBModels.db_rem(g)
            anonymous_questions = DBModels.AnonymousQuestion.query.filter_by(live_lecture_id=live_lecture.id).all()
            if anonymous_questions:
                for aq in anonymous_questions:
                    DBModels.db_rem(aq)
        polling_questions = DBModels.PollingQuestion.query.filter_by(lecture_id=lecture_id).all()
        if polling_questions:
            for pq in polling_questions:
                API.delete_polling_question(pq.id)
        lecture = DBModels.Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            DBModels.db_rem(lecture)
        return True

    # Delete a single class, class members, and lectures assoicated with the class
    @staticmethod
    def delete_class(class_id):
        lectures = DBModels.Lecture.query.filter_by(class_id=class_id).all()
        if lectures:
            for l in lectures:
                API.delete_lecture(l.id)
        class_members = DBModels.ClassMember.query.filter_by(class_id=class_id).all()
        if class_members:
            for cm in class_members:
                DBModels.db_rem(cm)
        classToDelete = DBModels.Class.query.filter_by(id=class_id).first()
        if classToDelete:
            DBModels.db_rem(classToDelete)
        return True

    # Removes student from a class and deletes all of the student's polling question responses
    @staticmethod
    def delete_class_student(student_id, class_id):
        entry = DBModels.ClassMember.query.filter_by(student_id=student_id, class_id=class_id).first()
        DBModels.db_rem(entry)
        lectures = DBModels.Lecture.query.filter_by(class_id=class_id).with_entities(DBModels.Lecture.id).all()
        lecture_ids = []
        for lecture in lectures:
            lecture_ids.append(lecture.id)

        polling_questions = DBModels.PollingQuestion.query.filter(DBModels.PollingQuestion.lecture_id.in_(lecture_ids)).all()
        polling_question_ids = []
        for q in polling_questions:
            polling_question_ids.append(q.id)
        polling_question_responses = DBModels.PollingQuestionResponse.query.filter( \
                DBModels.PollingQuestionResponse.polling_question_id.in_(polling_question_ids), \
                DBModels.PollingQuestionResponse.student_id==student_id).all()
        for resp in polling_question_responses:
            DBModels.db_rem(resp)
        return True

    # Removes student from a class and deletes all of the student's polling question responses
    @staticmethod
    def reset_gauges(live_lecture_id):
        liveLecture = DBModels.LiveLecture.query.filter_by(id=live_lecture_id).first()
        liveLecture.pace_total = 0
        liveLecture.depth_total= 0
        DBModels.db_update(liveLecture)
        gauges = DBModels.Gauge.query.filter_by(live_lecture_id=live_lecture_id)
        for gauge in gauges:
            gauge.depth = 0
            gauge.pace = 0
            DBModels.db_update(gauge)
        return True

    # Ends the the given live lecture
    @staticmethod
    def end_live_lecture(live_lecture_id):
        liveClass = DBModels.Class.query.filter_by(live_lecture_id=live_lecture_id).first()
        if liveClass is not None:
            liveClass.live_lecture_id = None
            return DBModels.db_update(liveClass)
        return False