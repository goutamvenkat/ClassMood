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

        # Create the user types
        studentType = UserType(STUDENT_TYPE, False, True)
        professorType = UserType(PROFESSOR_TYPE, True, True)
        db_add(studentType, professorType)

        # Create the users
        studentUser = User("Test", "Student", "student@gatech.edu", studentType.id)
        professorUser = User("Test", "Professor", "professor@gatech.edu", professorType.id)
        db_add(studentUser, professorUser)

        # Create the authentication for each user
        studentAuth = Authentication(studentUser.id, "password")
        professorAuth = Authentication(professorUser.id, "password")
        db_add(studentAuth, professorAuth)

        # Create the classes for the test professor
        cs101 = Class('CS 101', 'CS 101 with Test Professor', professorUser.id)
        cs102 = Class('CS 102', 'CS 102 with Test Professor', professorUser.id)
        cs103 = Class('CS 103', 'CS 103 with Test Professor', professorUser.id)
        cs201 = Class('CS 201', 'CS 201 with Test Professor', professorUser.id)
        db_add(cs101, cs102, cs103, cs201)

        # Add the test student to CS 101 and CS 102
        cs101Member = ClassMember(studentUser.id, cs101.id)
        cs102Member = ClassMember(studentUser.id, cs102.id)
        db_add(cs101Member, cs102Member)

        # Create a lecture for CS 101 and CS 102 and simulate voting up for pace and depth
        # Student is aleady a member of both classes, so he/she should be able to join lectures
        cs101Lecture = Lecture(cs101.id)
        cs102Lecture = Lecture(cs102.id)
        db_add(cs101Lecture, cs102Lecture)

        # Create gauge for student for CS 101, and simulate saying the lecture is too fast and vague
        cs101Gauge = Gauge(cs101.id, studentUser.id)
        cs101Gauge.depth = 1
        cs101Gauge.pace = 1
        # Create gauge for student for CS 102, and simulate saying the lecture is too slow and detailed
        cs102Gauge = Gauge(cs102.id, studentUser.id)
        cs102Gauge.depth = -1
        cs102Gauge.pace = -1
        db_add(cs101Gauge, cs102Gauge)

        # Update lecture properties for CS 101 and CS 102
        cs101Lecture.is_live = True
        cs101Lecture.pace_total = 1
        cs101Lecture.depth_total = 1
        cs101Lecture.num_students = 1
        cs102Lecture.is_live = True
        cs102Lecture.pace_total = -1
        cs102Lecture.depth_total = -1
        cs102Lecture.num_students = 1
        db_add(cs101Lecture, cs102Lecture)

        # Create anonymous question on behalf of student for both classes
        q1 = "Is Howey L1 the correct room for CS 101?"
        cs101AnonQuestion = AnonymousQuestion(cs101.id, q1, studentUser.id)
        q2 = "Is Howey L2 the correct room for CS 102?"
        cs102AnonQuestion = AnonymousQuestion(cs102.id, q2, studentUser.id)
        db_add(cs101AnonQuestion, cs102AnonQuestion)

from ClassMoodApp.Controllers import *