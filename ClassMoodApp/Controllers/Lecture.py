from ClassMoodApp import app
from flask import render_template, jsonify
from ClassMoodApp.Models.API import API
import json

@app.route('/live_lecture/create/<int:class_id>', methods = ['GET', 'POST'])
def create_live_lecture(class_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    prev = API.get_live_lecture(class_id)
    if prev:
        API.disable_live_lecture(prev)
    id = API.create_live_lecture(class_id)
    return json.dumps(id)

@app.route('/live_lecture/disable/<int:class_id>', methods = ['GET', 'POST'])
def disable_live_lecture(class_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.disable_live_lecture(class_id))

@app.route('/live_lecture/get/<int:class_id>', methods = ['GET', 'POST'])
def get_live_lecture(class_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.get_live_lecture(class_id))


@app.route('/live_lecture/add_student/<int:lect_id>', methods = ['GET', 'POST'])
def add_live_student(lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    s1 = API.add_student_to_lecture(lect_id)
    s2 = API.update_gauge_pace_and_depth(lect_id, authUser.id, 0, 0)
    ret = s1 and s2
    return json.dumps(ret)

@app.route('/live_lecture/pace/get/<int:lect_id>', methods = ['GET', 'POST'])
def get_curr_pace(lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.get_pace(lect_id))

@app.route('/live_lecture/depth/get/<int:lect_id>', methods = ['GET', 'POST'])
def get_curr_depth(lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.get_depth(lect_id))

@app.route('/live_lecture/gauge/get/<int:lect_id>', methods = ['GET', 'POST'])
def get_student_gauge(lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.get_gauge_pace_and_depth(lect_id, authUser.id))

@app.route('/live_lecture/gauge/put/<int:lect_id>/<string:pace_num>/<string:depth_num>', methods = ['GET', 'POST'])
def update_student_gauge(lect_id, pace_num, depth_num):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    try:
        pace_num = float(pace_num)
        depth_num = float(depth_num)
    except ValueError:
        return json.dumps(False)
    prev = API.get_gauge_pace_and_depth(lect_id, authUser.id)
    curr = (pace_num, depth_num)
    s1 = API.update_gauge_pace_and_depth(lect_id, authUser.id, pace_num, depth_num)
    s2 = API.change_total_pace_by(lect_id, curr[0] - prev[0])
    s3 = API.change_total_depth_by(lect_id, curr[1] - prev[1])
    ret = s1 and s2 and s3
    return json.dumps(ret)

@app.route('/live_lecture/questions/get/<int:lect_id>', methods = ['GET', 'POST'])
def get_anon_questions(lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.get_anonymous_questions(lect_id))

@app.route('/live_lecture/questions/put/<int:lect_id>/<string:text>', methods = ['GET', 'POST'])
def add_anon_question(lect_id, text):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.add_anonymous_question(lect_id, authUser.id, text))