from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template

@app.route("/login")
def login():
    testUser = User.query.filter_by(username="test_user").first()
    return render_template('authentication/login.html', user=testUser)