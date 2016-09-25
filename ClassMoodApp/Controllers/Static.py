from ClassMoodApp import app
from flask import render_template


@app.route("/test")
def test():
    return render_template('professorView/classList.html')

@app.route("/studentHomepage")
def test():
    return render_template('studentView/classList.html')

