from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request, session
from ClassMoodApp.Models.api import API

api = API()

@app.route("/")
def login():
    return render_template('authentication/login.html')

@app.route('/loginUser', methods=['POST'])
def loginUser():
    email = request.form['email']
    password = request.form['userpass']
    if api.is_login_valid(email, password):
        # at this point, render new template, get a new session token (if one doesn't exist)
        # and pass it along to the template.
        session_token = api.create_session(email)
        session["token"] = session_token
        #return redirect()
        return 'VALID'
    return render_template('authentication/login.html', error='Invalid email or password')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return render_template('authentication/login.html')