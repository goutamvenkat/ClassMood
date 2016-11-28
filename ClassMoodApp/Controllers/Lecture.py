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

@app.route('/lectureList/<int:class_id>', methods = ['GET', 'POST'])
def lect_list(class_id):
    return render_template('lectureList.html', classId=class_id, username=API.get_authentication().first_name)

@app.route('/pollingQuestionList/<int:class_id>/<int:lecture_id>', methods = ['GET', 'POST'])
def polling_questions_list(class_id, lecture_id):
    return render_template('pollingQuestionList.html', class_id=class_id, lecture_id=lecture_id, username=API.get_authentication().first_name)

@app.route('/pollingQuestionList/<int:class_id>/<int:lecture_id>/createPollingQuestion', methods = ['GET', 'POST'])
def get_polling_questions_list(class_id, lecture_id):
    username=API.get_authentication().first_name
    return render_template('createPollingQuestion.html', class_id=class_id, lecture_id=lecture_id, username=username)

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
    liveLectureId = API.get_live_lecture(class_id)
    lectureId = API.get_lecture_from_live_lecture(liveLectureId)
    if liveLectureId and lectureId:
        return render_template('liveView.html', username=API.get_authentication().first_name, user_id=API.get_authentication().id, lecture_id=lectureId, live_lecture_id=liveLectureId)

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

# student view get the current polling question
@app.route("/live_lecture/curr_polling_question/get/<int:live_lecture_id>", methods=['GET'])
def get_curr_polling_question(live_lecture_id):
    authUser = API.get_authentication()
    if not authUser:
        return jsonify(response="Not Authenticated")
    return json.dumps(API.get_current_polling_question(live_lecture_id))

# professor view. Changes the polling question. Returns success or not
@app.route('/live_lecture/present_polling_question/get/<int:live_lecture_id>/<int:polling_qid>', methods=['GET'])
def present_polling_question(live_lecture_id, polling_qid):
    authUser = API.get_authentication()
    if not authUser:
        return jsonify(response="Not Authenticated")
    return jsonify(success=API.present_polling_question(live_lecture_id, polling_qid))

@app.route('/live_lecture/respond_to_question/post', methods=['POST'])
def respond_to_polling_question():
    authUser = API.get_authentication()
    if not authUser:
        return jsonify(response="Not Authenticated")
    student_id = request.form.get('student_id')
    polling_qid = request.form.get('polling_qid')
    student_ans = request.form.get('student_ans')
    return jsonify(success=API.respond_to_polling_question(student_id, polling_qid, student_ans))

@app.route('/live_lecture/stop_polling_questions/<int:live_lecture_id>', methods=['GET'])
def stop_polling_questions(live_lecture_id):
    authUser = API.get_authentication()
    if not authUser:
        return jsonify(response="Not Authenticated")
    return json.dumps(API.stop_polling_questions(live_lecture_id))


@app.route('/get_lecture_list/<int:class_id>', methods = ['GET', 'POST'])
def get_lecture_list(class_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.get_lecture_list(class_id))

@app.route('/create_polling_question/<int:lecture_id>/<string:qtext>/<string:atext>/<string:btext>/<string:ctext>/<string:dtext>/<string:ans>', methods = ['GET', 'POST'])
def create_polling_question(lecture_id, qtext, atext, btext, ctext, dtext, ans):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.create_polling_question(lecture_id, qtext, atext, btext, ctext, dtext, ans))

@app.route('/get_polling_questions/<int:lecture_id>', methods = ['GET', 'POST'])
def get_polling_questions(lecture_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.get_polling_questions(lecture_id))

@app.route('/delete/polling_question/<int:polling_question_id>', methods = ['GET', 'POST'])
def delete_polling_question(polling_question_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.delete_polling_question(polling_question_id))

@app.route('/delete/lecture/<int:lecture_id>', methods = ['GET', 'POST'])
def delete_lecture(lecture_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.delete_lecture(lecture_id))

@app.route('/reset_gauges/<int:live_lecture_id>', methods = ['GET', 'POST'])
def reset_gauges(live_lecture_id):
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return jsonify(results=API.reset_gauges(live_lecture_id))