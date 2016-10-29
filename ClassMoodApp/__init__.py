from flask import Flask
from ClassMoodApp.Models.DBModels import *
from ClassMoodApp.Config.AppConfig import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
session = db.session

STUDENT_TYPE = "STUDENT"
PROFESSOR_TYPE = "PROFESSOR"

# If we are in testing mode, add some test data
if app.config.get('TESTING', False):
    with app.app_context():
        # Recreate the database
        db.drop_all()
        db.create_all()

        # Create the users
        studentUser = User("Test", "Student", "student@gatech.edu", True)
        otherStudentUser = User("Other", "Student", "other_student@gatech.edu", True)
        professorUser = User("Test", "Professor", "professor@gatech.edu", False)
        db_add(studentUser, otherStudentUser, professorUser)

        # Create the authentication for each user
        studentAuth = Authentication(studentUser.id, "password")
        otherStudentAuth = Authentication(otherStudentUser.id, "password")
        professorAuth = Authentication(professorUser.id, "password")
        db_add(studentAuth, otherStudentAuth, professorAuth)

        # Create the classes for the test professor
        cs101 = Class('CS 101', 'CS 101 with Test Professor', professorUser.id)
        cs102 = Class('CS 102', 'CS 102 with Test Professor', professorUser.id)
        cs103 = Class('CS 103', 'CS 103 with Test Professor', professorUser.id)
        cs201 = Class('CS 201', 'CS 201 with Test Professor', professorUser.id)
        db_add(cs101, cs102, cs103, cs201)

        # Add the test student to CS 101 and CS 102 using the class members table
        cs101Member = ClassMember(studentUser.id, cs101.id)
        cs101MemberOther = ClassMember(otherStudentUser.id, cs101.id)
        cs102Member = ClassMember(studentUser.id, cs102.id)
        db_add(cs101Member, cs101MemberOther, cs102Member)

        # Create two lectures for cs101 and a lecture for cs102
        cs101LectureA = Lecture('Lecture A', cs101.id)
        cs101LectureB = Lecture('Lecture B', cs101.id)
        cs102Lecture = Lecture('Lecture', cs102.id)
        db_add(cs101LectureA, cs101LectureB, cs102Lecture)

        # Create a live lecture for cs101 from Lecture A and a live lecture for cs102 from Lecture
        cs101LiveLecture = LiveLecture(cs101LectureA.id)
        cs102LiveLecture = LiveLecture(cs102Lecture.id)
        # Update lecture properties for CS 101 and CS 102
        cs101LiveLecture.pace_total = -2
        cs101LiveLecture.depth_total = 1
        cs101LiveLecture.num_students = 2
        cs102LiveLecture.pace_total = -1
        cs102LiveLecture.depth_total = -1
        cs102LiveLecture.num_students = 1
        db_add(cs101LiveLecture, cs102LiveLecture)

        # Create two gauges for students in CS 101
        cs101Gauge = Gauge(cs101LiveLecture.id, studentUser.id)
        cs101Gauge.pace = -1
        cs101Gauge.depth = 1
        cs101GaugeOther = Gauge(cs101LiveLecture.id, otherStudentUser.id)
        cs101GaugeOther.pace = -1
        cs101GaugeOther.depth = 0
        # Create gauge for a student in CS 102
        cs102Gauge = Gauge(cs102LiveLecture.id, studentUser.id)
        cs102Gauge.pace = -1
        cs102Gauge.depth = -1
        db_add(cs101Gauge, cs101GaugeOther, cs102Gauge)

        # Update the cs101 and cs102 classes to point to the current live lectures
        cs101.live_lecture_id = cs101LiveLecture.id
        cs102.live_lecture_id = cs102LiveLecture.id
        db_update(cs101, cs102)

        # Create anonymous question on behalf of student for both classes
        q1 = "Is Howey L1 the correct room for CS 101?"
        cs101AnonQuestion = AnonymousQuestion(cs101LiveLecture.id, q1, studentUser.id)
        q2 = "Is Howey L2 the correct room for CS 102?"
        cs102AnonQuestion = AnonymousQuestion(cs102LiveLecture.id, q2, otherStudentUser.id)
        db_add(cs101AnonQuestion, cs102AnonQuestion)

        # Create an anonymous question for each lecture
        cs101LectureAQuestion = PollingQuestion(cs101LectureA.id, "What The correct room for this class?", "Howey L1", "Howey L2", "", "", "A")
        cs101LectureBQuestion = PollingQuestion(cs101LectureB.id, "What is the name of this class?", "CS 103", "CS 102", "CS 101", "", "C")
        cs102LectureQuestion = PollingQuestion(cs102Lecture.id, "What The correct room for this class?", "Howey L1", "Howey L2", "", "", "B")
        db_add(cs101LectureAQuestion, cs101LectureBQuestion, cs102LectureQuestion)

        # Create two responses for cs 101 lecture A question
        cs101LectureAQuestionResponse = PollingQuestionResponse(studentUser.id, cs101LectureAQuestion.id, "A")
        cs101LectureAQuestionResponseOther = PollingQuestionResponse(otherStudentUser.id, cs101LectureAQuestion.id, "C")
        # Create a response for cs 102 lecture question
        cs102LectureQuestionResponse = PollingQuestionResponse(studentUser.id, cs102LectureQuestion.id, "B")
        db_add(cs101LectureAQuestionResponse, cs101LectureAQuestionResponseOther, cs102LectureQuestionResponse)

# from ClassMoodApp.Controllers import *