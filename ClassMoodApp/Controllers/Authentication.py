from ClassMoodApp import app
from flask import render_template, request, session, jsonify
from ClassMoodApp.Models.API import API

login_page = 'authentication/login.html'
main_page = 'classList.html'

@app.route("/")
def login():
    if API.get_authentication():
        return render_template(main_page, username=API.get_authentication().first_name, user_id=API.get_authentication().id)
    return render_template(login_page)

@app.route('/loginUser', methods=['POST'])
def loginUser():
    email = request.form['email']
    password = request.form['userpass']
    user = API.validate_login(email, password)
    if user:
        session_token = API.create_session(user.id)
        if not session_token:
            return render_template(login_page, error='Failed to create token')
        session["token"] = session_token
        return render_template(main_page, username=API.get_authentication().first_name, user_id=API.get_authentication().id)

    return render_template(login_page, error='Invalid email or password')

@app.route('/logoutUser', methods=['GET', 'POST'])
def logout():
    token = session["token"]
    API.delete_session(token)
    session.pop('token', None)
    return render_template(login_page, message='You have been logged out')

@app.route('/user_id', methods=['GET'])
def user_id():
    auth = API.get_authentication()
    if auth:
        return jsonify(results=auth.id)
    return jsonify(results=[])