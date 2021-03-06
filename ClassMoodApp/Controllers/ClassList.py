from ClassMoodApp import app
from flask import render_template, jsonify
from ClassMoodApp.Models.API import API
import json

login_page = 'authentication/login.html'
main_page = 'classList.html'

# Returns a template for the class list page
@app.route('/classList', methods=['GET'])
def classList():
    authUser = API.get_authentication()
    if not authUser:
        return render_template(login_page, error='You are not logged in')
    return render_template(main_page, username=API.get_authentication().first_name, user_id=API.get_authentication().id)

# Returns the list of classes for the current user
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
            class_info.append({'className': each_class, 'id' : class_id, 'liveLectureId': live_lecture_id, 'is_live': True})
        else:
            class_info.append({'className': each_class, 'id' : class_id, 'liveLectureId': live_lecture_id, 'is_live': False})
    return jsonify(results=class_info)

# Returns if the current user is a student
@app.route('/is_student', methods=['GET'])
def is_student():
    authUser = API.get_authentication()
    if not authUser:
        return render_template(login_page, error='You are not logged in')
    return jsonify(results=API.is_student(authUser.id))

# Creates a class with the given class name
@app.route('/createClass/<className>', methods=['GET','POST'])
def createClass(className):
    authUser = API.get_authentication()
    if not authUser:
        return render_template(login_page, error='You are not logged in')
    return json.dumps(API.create_prof_class(className, authUser.id))

# Adds a class for the student
@app.route('/set_student_classes/<class_name>/<int:student_id>', methods = ['GET', 'POST'])
def set_student_classes(class_name, student_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.set_student_class(class_name, student_id))

# Deletes a class and all associations with it
@app.route('/delete/class/<int:class_id>', methods = ['GET', 'POST'])
def delete_class(class_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.delete_class(class_id))

# Removes a class from a student
@app.route('/delete/class_student/<int:student_id>/<int:class_id>', methods = ['GET', 'POST'])
def delete_class_student(student_id, class_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.delete_class_student(student_id, class_id))