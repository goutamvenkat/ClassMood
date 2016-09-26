from ClassMoodApp import app
from flask import render_template
from ClassMoodApp.Models.api import API

api = API()

@app.route("/professorHomepage")
def prof_home():
    authUser = api.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return render_template('professorView/classList.html')

@app.route("/studentHomepage")
def stud_home():
    authUser = api.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return render_template('studentView/classList.html')
