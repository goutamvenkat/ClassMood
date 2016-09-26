from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request, jsonify
from ClassMoodApp.Models.api import API
import json

api = API()

@app.route('/getProfessorClassList', methods=['GET'])
def getProfessorClassList():
    authUser = api.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    professorEmail = authUser.email
    classList = api.get_professor_class_list(professorEmail)
    if classList is None:
        classList = []
    return jsonify(results=classList)

@app.route('/createClass/<className>', methods=['POST'])
def createClass(className):
    authUser = api.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    professorEmail = authUser.email
    successful = api.create_prof_lecture(className, professorEmail)
    if successful:
        return 'True'
    else:
        return 'False'

@app.route('/prof_lectures', methods=['GET'])
def prof_lectures():
    professor_email = 'test@test.com' # get from session token
    lecture_list = api.get_professor_class_list(professor_email)
    return jsonify(results=lecture_list)

@app.route('/create_class/<class_name>', methods=['POST'])
def create_class(class_name):
    professor_email = 'test@test.com'; # get from session token
    successful = api.create_prof_lecture(class_name, professor_email)
    return json.dumps(successful)

@app.route('/student_lectures/<int:student_id>', methods = ['GET'])
def student_lectures(student_id):
    lecture_list = api.get_student_lecture_list(student_id)
    return jsonify(results = lecture_list)

@app.route('/set_student_lectures/<lecture_name>/<int:student_id>', methods = ['POST'])
def set_student_lectures(lecture_name, student_id):
    return json.dumps(api.set_student_lecture(lecture_name, student_id))
