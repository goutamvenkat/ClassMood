from ClassMoodApp import app
from flask import render_template, jsonify
from ClassMoodApp.Models.API import API
import json

login_page = 'authentication/login.html'

# @app.route('/getProfessorClassList', methods=['GET'])
# def getProfessorClassList():
#     authUser = API.get_authentication()
#     if not authUser:
#         return render_template('authentication/login.html', error='You are not logged in')
#     classList = API.get_professor_class_list(authUser.id)
#     if classList is None:
#         classList = []
#     return jsonify(results=classList)

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

# @app.route('/student_classes/<int:student_id>', methods = ['GET'])
# def student_classes(student_id):
#     class_list = API.get_student_class_list(student_id)
#     return jsonify(results = class_list)



@app.route('/set_student_classes/<class_name>/<int:student_id>', methods = ['GET', 'POST'])
def set_student_classes(class_name, student_id):
    return json.dumps(API.set_student_class(class_name, student_id))
