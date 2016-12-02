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
        studentUser1 = User("Neil", "Vohra", "neilvohra@gatech.edu", True)
        studentUser2 = User("Goutam", "Venkat", "goutamvenkat@gatech.edu", True)
        professorUser = User("Kevin", "Han", "professor@gatech.edu", False)
        db_add(studentUser1, studentUser2, professorUser)

        # Create the authentication for each user
        student1Auth = Authentication(studentUser1.id, "password")
        student2Auth = Authentication(studentUser2.id, "password")
        professorAuth = Authentication(professorUser.id, "password")
        db_add(student1Auth, student2Auth, professorAuth)

        # Create the classes for the test professor
        cs1332 = Class('CS 1332', 'CS 2200 with Kevin Han', professorUser.id)
        cs4001 = Class('CS 4001', 'CS 4001 with Kevin Han', professorUser.id)
        # cs2200 = Class('CS 2200', 'CS 2200 with Test Professor', professorUser.id)
        cs4140 = Class('CS 4140/6140', 'CS 4140/6140 with Kevin han', professorUser.id)
        db_add(cs1332, cs4001, cs4140)

        # # Add the test student to CS 1332 and CS 220 using the class members table
        # cs1332Member = ClassMember(studentUser1.id, cs1332.id)
        # cs1332MemberOther = ClassMember(otherStudentUser.id, cs1332.id)
        # cs2200Member = ClassMember(studentUser.id, cs2200.id)
        # db_add(cs1332Member, cs1332MemberOther, cs2200Member)

        # # Create two lectures for cs1332 and a lecture for cs2200
        # cs1332LectureA = Lecture('Lecture A', cs1332.id)
        # cs1332LectureB = Lecture('Lecture B', cs1332.id)
        # cs2200Lecture = Lecture('Lecture', cs2200.id)
        # db_add(cs1332LectureA, cs1332LectureB, cs2200Lecture)

        # # Create a live lecture for cs1332 from Lecture A and a live lecture for cs2200 from Lecture
        # cs1332LiveLecture = LiveLecture(cs1332LectureA.id)
        # cs2200LiveLecture = LiveLecture(cs2200Lecture.id)
        # # Update lecture properties for CS 101 and CS 102
        # cs1332LiveLecture.pace_total = -2
        # cs1332LiveLecture.depth_total = 1
        # cs1332LiveLecture.num_students = 2
        # cs2200LiveLecture.pace_total = -1
        # cs2200LiveLecture.depth_total = -1
        # cs2200LiveLecture.num_students = 1
        # db_add(cs1332LiveLecture, cs2200LiveLecture)

        # # Create two gauges for students in CS 101
        # cs1332Gauge = Gauge(cs1332LiveLecture.id, studentUser.id)
        # cs1332Gauge.pace = -1
        # cs1332Gauge.depth = 1
        # cs1332GaugeOther = Gauge(cs1332LiveLecture.id, otherStudentUser.id)
        # cs1332GaugeOther.pace = -1
        # cs1332GaugeOther.depth = 0
        # # Create gauge for a student in CS 102
        # cs2200Gauge = Gauge(cs2200LiveLecture.id, studentUser.id)
        # cs2200Gauge.pace = -1
        # cs2200Gauge.depth = -1
        # db_add(cs1332Gauge, cs1332GaugeOther, cs2200Gauge)

        # # Update the cs1332 and cs2200 classes to point to the current live lectures
        # cs1332.live_lecture_id = cs1332LiveLecture.id
        # cs2200.live_lecture_id = cs2200LiveLecture.id
        # db_update(cs1332, cs2200)

        # # Create anonymous question on behalf of student for both classes
        # q1 = "Is Howey L1 the correct room for CS 101?"
        # cs1332AnonQuestion = AnonymousQuestion(cs1332LiveLecture.id, q1, studentUser.id)
        # q2 = "Is Howey L2 the correct room for CS 102?"
        # cs2200AnonQuestion = AnonymousQuestion(cs2200LiveLecture.id, q2, otherStudentUser.id)
        # db_add(cs1332AnonQuestion, cs2200AnonQuestion)

        # # Create an anonymous question for each lecture
        # cs1332LectureAQuestion = PollingQuestion(cs1332LectureA.id, "What is the correct room for this class?", "Howey L1", "Howey L2", "", "", "A")
        # cs1332LectureAQuestion2 = PollingQuestion(cs1332LectureA.id, "What is 2+2?", "1", "2", "3", "4", "D")
        # cs1332LectureBQuestion = PollingQuestion(cs1332LectureB.id, "What is the name of this class?", "CS 103", "CS 102", "CS 101", "", "C")
        # cs2200LectureQuestion = PollingQuestion(cs2200Lecture.id, "What The correct room for this class?", "Howey L1", "Howey L2", "", "", "B")
        # db_add(cs1332LectureAQuestion, cs1332LectureAQuestion2, cs1332LectureBQuestion, cs2200LectureQuestion)

        # # Create two responses for cs 101 lecture A question
        # cs1332LectureAQuestionResponse = PollingQuestionResponse(studentUser.id, cs1332LectureAQuestion.id, "A")
        # cs1332LectureAQuestionResponseOther = PollingQuestionResponse(otherStudentUser.id, cs1332LectureAQuestion.id, "C")
        # # Create a response for cs 102 lecture question
        # cs2200LectureQuestionResponse = PollingQuestionResponse(studentUser.id, cs2200LectureQuestion.id, "B")
        # db_add(cs1332LectureAQuestionResponse, cs1332LectureAQuestionResponseOther, cs2200LectureQuestionResponse)

from ClassMoodApp.Controllers import *