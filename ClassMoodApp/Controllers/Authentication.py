from ClassMoodApp import app
from flask import render_template, request, session, jsonify, redirect
from ClassMoodApp.Models.API import API

login_page = 'authentication/login.html'
main_page = 'classList.html'

@app.route("/")
def login():
    if API.get_authentication():
        return render_template(main_page, username=API.get_authentication().first_name, user_id=API.get_authentication().id)
    return render_template(login_page)

@app.route('/loginUser', methods=['POST'])
@app.route('/loginUser/<email>/<name>', methods=['GET', 'POST'])
def loginUser(email=None, name=None):
    user = None
    if not email and not name:
        email = request.form['email']
        password = request.form['userpass']
        user = API.validate_login(email, password)
    elif email and name:
        user = API.get_google_user(email, name)
    if user:
        session_token = API.create_session(user.id)
        if not session_token:
            return render_template(login_page, error='Failed to create token')
        session["token"] = session_token
        return render_template(main_page, username=API.get_authentication().first_name, user_id=API.get_authentication().id)
    return render_template(login_page, error='Invalid email or password')

@app.route('/logoutUser', methods=['GET', 'POST'])
def logout():
    user = API.get_authentication()
    token = session["token"]
    API.delete_session(token)
    session.pop("token", None)
    # return redirect(url_for('login'))
    return render_template(login_page, message='You have been logged out')

@app.route('/user_id', methods=['GET'])
def user_id():
    auth = API.get_authentication()
    if auth:
        return jsonify(results=auth.id)
    return jsonify(results=[])

@app.route('/is_google_user', methods=['GET'])
def is_google_user():
    return jsonify(results=API.is_google_account())