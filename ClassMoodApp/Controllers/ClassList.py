from ClassMoodApp import app
from ClassMoodApp.Models.DBModels import User
from flask import render_template, request
from ClassMoodApp.Models.api import API
from flask import jsonify

api = API()

@app.route('/getProfessorClassList', methods=['GET'])
def getProfessorClassList():
	return jsonify(results=['class2', 'class5', 'class3']) # remove
	
	professorEmail = 'test@test.com' # get from session token
	classList = api.get_professor_class_list(professorEmail)
	if classList is None:
		classList = []
	return jsonify(results=classList)

@app.route('/createClass', methods=['POST'])
def createClass():
	className = 'testclass';
	professorEmail = 'test@test.com'; #get from session token
	return api.create_class()