from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request, session, url_for
from ClassMoodApp.Models.api import API

api = API()

@app.route("/")
def login():
    if api.get_authentication():
        return render_template('authentication/authtest.html', error='You are already logged in')
    return render_template('authentication/login.html')

@app.route('/loginUser', methods=['POST'])
def loginUser():
    email = request.form['email']
    password = request.form['userpass']
    user = api.validate_login(email, password)
    if user:
        session_token = api.create_session(user.id)
        if not session_token:
            return render_template('authentication/login.html', error='Failed to create token')
        session["token"] = session_token
        usertype = api.get_access(user.user_type)
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
    api.delete_session(token)
    session.pop('token', None)
    return render_template('authentication/login.html', error='You have been logged out')
