from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request,
from ClassMoodApp.Models.api import API

api = API()

@app.route("/")
def login():
    if api.is_authenticated():
        return render_template('authentication/authtest.html', error='You are already logged in')
    return render_template('authentication/login.html')

@app.route('/loginUser', methods=['POST'])
def loginUser():
    email = request.form['email']
    password = request.form['userpass']
    if api.is_login_valid(email, password):
        # at this point, render new template, get a new session token (if one doesn't exist)
        # and pass it along to the template.
        session_token = api.create_session(email)
        if not session_token:
            return render_template('authentication/login.html', error='Failed to create token')
        session["token"] = session_token
        #return redirect()
        return render_template('authentication/authtest.html', error='You are now logged in')
    return render_template('authentication/login.html', error='Invalid email or password')

@app.route('/logoutUser', methods=['POST'])
def logout():
    token = session["token"]
    api.delete_session(token)
    session.pop('token', None)
    return render_template('authentication/login.html', error='You have been logged out')