from flask import Flask
from ClassMoodApp.Models.DBModels import db
from ClassMoodApp.Models.DBModels import UserType, User, Authentication, Class, ClassMember
from ClassMoodApp.Config.AppConfig import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

# If we are in testing mode, add some test data
if app.config.get('TESTING', False):
    with app.app_context():
        # Recreate the database
        db.drop_all()
        db.create_all()

        # Create the user types
        studentType = UserType("STUDENT", False, True)
        db.session.add(studentType)
        professorType = UserType("PROFESSOR", True, True)
        db.session.add(professorType)
        db.session.commit()

        # Create the users
        studentUser = User("Test", "Student", "student@gatech.edu", studentType.id)
        db.session.add(studentUser)
        professorUser = User("Test", "Professor", "professor@gatech.edu", professorType.id)
        db.session.add(professorUser)
        db.session.commit()

        # Create the authentication for each user
        studentAuth = Authentication(studentUser.id, "password")
        db.session.add(studentAuth)
        professorAuth = Authentication(professorUser.id, "password")
        db.session.add(professorAuth)
        db.session.commit()

        # Create the classes for the test professor
        class101 = Class('CS 101', 'CS 101 with Test Professor', professorUser.id)
        db.session.add(class101)
        class102 = Class('CS 102', 'CS 102 with Test Professor', professorUser.id)
        db.session.add(class102)
        class103 = Class('CS 103', 'CS 103 with Test Professor', professorUser.id)
        db.session.add(class103)
        class201 = Class('CS 201', 'CS 201 with Test Professor', professorUser.id)
        db.session.add(class201)
        db.session.commit()

        # Add the test student to CS 101 and CS 102
        cs101Member = ClassMember(studentUser.id, class101.id)
        db.session.add(cs101Member)
        cs102Member = ClassMember(studentUser.id, class102.id)
        db.session.add(cs102Member)
        db.session.commit()

from ClassMoodApp.Controllers import *