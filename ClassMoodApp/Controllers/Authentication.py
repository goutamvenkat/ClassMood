from ClassMoodApp import app
from flask import render_template, request, session, jsonify
from ClassMoodApp.Models.API import API

@app.route("/")
def login():
    if API.get_authentication():
        return render_template('authentication/authtest.html', error='You are already logged in')
    return render_template('authentication/login.html')

@app.route('/loginUser', methods=['POST'])
def loginUser():
    email = request.form['email']
    password = request.form['userpass']
    user = API.validate_login(email, password)
    if user:
        session_token = API.create_session(user.id)
        if not session_token:
            return render_template('authentication/login.html', error='Failed to create token')
        session["token"] = session_token
        usertype = API.get_access(user.user_type)
        if usertype.name == "STUDENT":
            return render_template('studentView/classList.html')
            # return render_template(url_for('stud_home'))
        elif usertype.name == "PROFESSOR":
            return render_template('professorView/classList.html')
            # return render_template(url_for("prof_home"))

    return render_template("authentication/login.html", error='Invalid email or password')

@app.route('/logoutUser', methods=['POST'])
def logout():
    token = session["token"]
    API.delete_session(token)
    session.pop('token', None)
    return render_template('authentication/login.html', error='You have been logged out')

@app.route('/getAuth', methods=['GET'])
def get_auth():
    usr = API.get_authentication()
    if usr:
        perms = API.get_access(usr.user_type)
        ret = perms.__dict__
        ret['id'] = usr.id #replace usertype id with user id
        del ret['_sa_instance_state'] #remove SQLalchemy data
    else:
        ret = {}
    return jsonify(results=ret)