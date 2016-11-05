from ClassMoodApp import app
from flask import render_template, jsonify, request
from ClassMoodApp.Models.API import API
import json

@app.route('/add_lecture/<int:class_id>/<lecture_name>', methods=['GET', 'POST'])
def add_lecture(class_id, lecture_name):
    new_lecture_id = API.create_lecture(lecture_name, class_id)
    return json.dumps(new_lecture_id)

@app.route('/join_live_lecture/<int:live_lecture_id>', methods=['GET', 'POST'])
def join_lecture(live_lecture_id):
    return json.dumps(API.add_student_to_live_lecture(live_lecture_id))

@app.route('/live_lecture/create/<int:lecture_id>', methods = ['GET', 'POST'])
def create_live_lecture(lecture_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.create_live_lecture(lecture_id))

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
    lectureId = API.get_live_lecture(class_id)
    if lectureId is not None:
        return render_template('liveView.html', username=API.get_authentication().first_name, user_id=API.get_authentication().id, lecture_id=lectureId)

@app.route('/live_lecture/add_student/<int:live_lect_id>', methods = ['GET', 'POST'])
def add_live_student(live_lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    s1 = API.add_student_to_live_lecture(live_lect_id)
    s2 = API.update_gauge_pace_and_depth(live_lect_id, authUser.id, 0, 0)
    ret = s1 and s2
    return json.dumps(ret)

@app.route('/live_lecture/pace/get/<int:live_lect_id>', methods = ['GET', 'POST'])
def get_curr_pace(live_lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.get_pace(live_lect_id))

@app.route('/live_lecture/depth/get/<int:live_lect_id>', methods = ['GET', 'POST'])
def get_curr_depth(live_lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.get_depth(live_lect_id))

@app.route('/live_lecture/gauge/get/<int:live_lect_id>', methods = ['GET', 'POST'])
def get_student_gauge(live_lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.get_gauge_pace_and_depth(live_lect_id, authUser.id))

@app.route('/live_lecture/gauge/put/<int:live_lect_id>/<string:pace_num>/<string:depth_num>', methods = ['GET', 'POST'])
def update_student_gauge(live_lect_id, pace_num, depth_num):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    try:
        json_data = request.get_json()
        lect_id = int(json_data['lect_id'])
        pace_num = float(json_data['pace_num'])
        depth_num = float(json_data['depth_num'])
    except ValueError:
        return json.dumps(False)
    prev = API.get_gauge_pace_and_depth(live_lect_id, authUser.id)
    curr = (pace_num, depth_num)
    s1 = API.update_gauge_pace_and_depth(live_lect_id, authUser.id, pace_num, depth_num)
    s2 = API.change_total_pace_by(live_lect_id, curr[0] - prev[0])
    s3 = API.change_total_depth_by(live_lect_id, curr[1] - prev[1])
    ret = s1 and s2 and s3
    return json.dumps(ret)

@app.route('/live_lecture/questions/get/<int:live_lect_id>', methods = ['GET', 'POST'])
def get_anon_questions(live_lect_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.get_anonymous_questions(live_lect_id))

@app.route('/live_lecture/questions/put/<int:live_lect_id>/<string:text>', methods = ['GET', 'POST'])
def add_anon_question(live_lect_id, text):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return json.dumps(API.add_anonymous_question(live_lect_id, authUser.id, text))