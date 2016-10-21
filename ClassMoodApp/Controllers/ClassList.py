from ClassMoodApp import app
from flask import render_template, jsonify
from ClassMoodApp.Models.API import API
import json

login_page = 'authentication/login.html'

@app.route('/getClassList', methods=['GET'])
def getClassList():
    authUser = API.get_authentication()
    if not authUser:
        return render_template(login_page, error='You are not logged in')
    class_list = []
    if API.is_student(authUser.id):
        class_list = API.get_student_class_list(authUser.id)
    else:
        class_list = API.get_professor_class_list(authUser.id)
    class_info = []
    for each_class in class_list:
        class_id = API.get_class_id(each_class)
        live_lecture_id = API.get_live_lecture(class_id)
        if live_lecture_id:
            class_info.append({'className': each_class, 'liveLectureId': live_lecture_id, 'is_live': True})
        else:
            class_info.append({'className': each_class, 'liveLectureId': live_lecture_id, 'is_live': False})
    return jsonify(results=class_info)

@app.route('/is_student', methods=['GET'])
def is_student():
    authUser = API.get_authentication()
    if not authUser:
        return render_template(login_page, error='You are not logged in')
    return jsonify(results=API.is_student(authUser.id))

@app.route('/createClass/<className>', methods=['POST'])
def createClass(className):
    authUser = API.get_authentication()
    if not authUser:
        return render_template(login_page, error='You are not logged in')
    return json.dumps(API.create_prof_class(className, authUser.id))

@app.route('/add_lecture/<class_name>')
def add_lecture(class_name):
    class_id = API.get_class_id(class_name)    
    new_lecture_id = API.create_live_lecture(class_id)
    return json.dumps(new_lecture_id)

@app.route('/join_lecture/<int:lecture_id>')
def join_lecture(lecture_id):
    return json.dumps(API.add_student_to_lecture(lecture_id))

@app.route('/set_student_classes/<class_name>/<int:student_id>', methods = ['GET', 'POST'])
def set_student_classes(class_name, student_id):
    return json.dumps(API.set_student_class(class_name, student_id))
