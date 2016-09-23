from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request, jsonify
from ClassMoodApp.Models.api import API

api = API()

@app.route('/getProfessorClassList', methods=['GET'])
def getProfessorClassList():
	return jsonify(results=['class2', 'class5', 'class3']) # remove
	
	professorEmail = 'test@test.com' # get from session token
	classList = api.get_professor_class_list(professorEmail)
	if classList is None:
		classList = []
	return jsonify(results=classList)

@app.route('/createClass/<className>', methods=['POST'])
def createClass(className):
	professorEmail = 'test@test.com'; #get from session token
	successful = api.create_class(className, professorEmail)
	if successful:
		return "True"
	else:
		return "False"