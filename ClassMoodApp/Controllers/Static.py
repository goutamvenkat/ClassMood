from ClassMoodApp import app
from flask import render_template

@app.route("/studentHomepage")
def test():
    return render_template('studentView/classList.html')