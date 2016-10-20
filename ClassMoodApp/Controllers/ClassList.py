from ClassMoodApp import app
from flask import render_template, jsonify
from ClassMoodApp.Models.API import API
import json

@app.route('/getProfessorClassList', methods=['GET'])
def getProfessorClassList():
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    classList = API.get_professor_class_list(authUser.id)
    if classList is None:
        classList = []
    return jsonify(results=classList)

@app.route('/createClass/<className>', methods=['POST'])
def createClass(className):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.create_prof_class(className, authUser.id))

@app.route('/student_classes/<int:student_id>', methods = ['GET'])
def student_classes(student_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    class_list = API.get_student_class_list(student_id)
    return jsonify(results = class_list)

@app.route('/set_student_classes/<class_name>/<int:student_id>', methods = ['POST'])
def set_student_classes(class_name, student_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.set_student_class(class_name, student_id))

