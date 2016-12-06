from ClassMoodApp import app
from flask import render_template
from ClassMoodApp.Models.API import API

# Returns a template for the homepage for a professor
@app.route("/professorHomepage")
def prof_home():
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return render_template('professorView/classList.html')

# Returns a template for the homepage for a student
@app.route("/studentHomepage")
def stud_home():
    authUser = API.get_authentication()
    if not authUser:
        return render_template('authentication/login.html', error='You are not logged in')
    return render_template('studentView/classList.html')
