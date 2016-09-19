from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request
from ClassMoodApp.Models.api import API

api = API()

@app.route('/getProfessorClassList', methods=['GET'])
def getProfessorClassList():
	professorEmail = 'test@test.com' # get from session token
	classList = get_professor_class_list(professorEmail)
	return ['class1', 'class2', 'class3'] # remove
	if classList is None:
		return []
	else:
		return classList