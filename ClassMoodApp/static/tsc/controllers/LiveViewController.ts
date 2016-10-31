/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
	"use strict";
	export class LiveViewController {
		static $inject = ["$scope", "$http", "$timeout"];
		public isStudent: boolean;
		public questions: AnonymousQuestionsModel;
		public questionEntered: string;
		private userId: number;
		private lectureId: number;
		constructor(private $scope: ng.IScope,
					private $http: ng.IHttpService,
					private $timeout: ng.ITimeoutService) {
						this.$http = $http;
						this.$scope = $scope;
						this.getIsStudent();
						this.getUserId();
						this.getLectureId();
						this.questionEntered = '';
						this.questions = new AnonymousQuestionsModel();
						this.questions.questions_array = [];
						this.questions.questions_string = '';
					}

		private getIsStudent(): void {
			this.$http.get("/is_student").success(
                (is_student: any) => {
                    this.isStudent = is_student.results;
                	
                	if (!this.isStudent) {
                		this.pollAnonymousQuestions(this);
                	}
            
            	}
            )
		}

		private getUserId(): void {
			this.$http.get('/user_id').then(
				(response: any) => {
					this.userId = response.data.results;
				}
			)
		}

		private getLectureId(): void {
			this.lectureId = parseInt($("#lectureId").attr('lecture-id'), 10);
		}

		private pollAnonymousQuestions(self): void {
			this.$http.get(`/live_lecture/questions/get/${this.lectureId}`)
			.success(function(response: any) {
				console.log(response);
				self.questions.questions_array = response.results;
				self.questions.questions_string = self.questions.questions_array.join('\n');
				self.$timeout(function() {self.pollAnonymousQuestions(self)}, 5000);
			})
			.error(function(response: any) {
				self.$timeout(function() {self.pollAnonymousQuestions(self)}, 10000);
			})
		}

		private submitPressed(): void {
			this.submitAnonymousQuestion(this);
		}

		private submitAnonymousQuestion(self): void {
			if (this.questionEntered !== '') {
				this.$http.get(`/live_lecture/questions/put/${this.lectureId}/${this.questionEntered}`)
				.success(function (response: boolean) {
					self.questions.questions_array.push(self.questionEntered);
					self.questions.questions_string = self.questions.questions_array.join('\n');
					self.questionEntered = '';
				})
			}
		}



	}
	app.controller('LiveViewController', LiveViewController);
}