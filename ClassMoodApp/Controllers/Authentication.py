from ClassMoodApp import app
from flask import render_template, request, session, jsonify, redirect, make_response
from ClassMoodApp.Models.API import API

login_page = 'authentication/login.html'
main_page = 'classList.html'

# Returns a template for the login page
@app.route("/")
def login():
    if API.get_authentication():
        return render_template(main_page, username=API.get_authentication().first_name, user_id=API.get_authentication().id)
    return render_template(login_page)

# Authenticates the user. Returns the homepage if authenticated successfully, otherwise an error
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
        resp = make_response(render_template(main_page, 
                                            username=API.get_authentication(session_token).first_name,
                                            user_id=API.get_authentication(session_token).id))
        resp.set_cookie('token', str(session_token))
        return resp
    return render_template(login_page, error='Invalid email or password')

# Logs the user out of the application
@app.route('/logoutUser', methods=['GET', 'POST'])
def logout():
    session_token = request.cookies.get('token')
    API.delete_session(session_token)
    resp = make_response(render_template(login_page, message='You have been logged out'))
    resp.set_cookie('token', '')
    return resp

# Returns the user id of the current user
@app.route('/user_id', methods=['GET'])
def user_id():
    auth = API.get_authentication()
    if auth:
        return jsonify(results=auth.id)
    return jsonify(results=[])

# Returns if the current user is logged in via Google
@app.route('/is_google_user', methods=['GET'])
def is_google_user():
    return jsonify(results=API.is_google_account())