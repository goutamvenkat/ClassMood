/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var LiveViewController = (function () {
        function LiveViewController($scope, $http, $timeout) {
            this.$scope = $scope;
            this.$http = $http;
            this.$timeout = $timeout;
            this.$http = $http;
            this.$scope = $scope;
            this.getIsStudent();
            this.getUserId();
            this.getLectureId();
            this.questionEntered = '';
            this.questions = new ClassMoodApp.AnonymousQuestionsModel();
            this.questions.questions_array = [];
            this.questions.questions_string = '';
        }
        LiveViewController.prototype.getIsStudent = function () {
            var _this = this;
            this.$http.get("/is_student").success(function (is_student) {
                _this.isStudent = is_student.results;
                if (!_this.isStudent) {
                    _this.pollAnonymousQuestions(_this);
                }
            });
        };
        LiveViewController.prototype.getUserId = function () {
            var _this = this;
            this.$http.get('/user_id').then(function (response) {
                _this.userId = response.data.results;
            });
        };
        LiveViewController.prototype.getLectureId = function () {
            this.lectureId = parseInt($("#lectureId").attr('lecture-id'), 10);
        };
        LiveViewController.prototype.pollAnonymousQuestions = function (self) {
            this.$http.get("/live_lecture/questions/get/" + this.lectureId)
                .success(function (response) {
                console.log(response);
                self.questions.questions_array = response.results;
                self.questions.questions_string = self.questions.questions_array.join('\n');
                self.$timeout(function () { self.pollAnonymousQuestions(self); }, 5000);
            })
                .error(function (response) {
                self.$timeout(function () { self.pollAnonymousQuestions(self); }, 10000);
            });
        };
        LiveViewController.prototype.submitPressed = function () {
            this.submitAnonymousQuestion(this);
        };
        LiveViewController.prototype.submitAnonymousQuestion = function (self) {
            if (this.questionEntered !== '') {
                this.$http.get("/live_lecture/questions/put/" + this.lectureId + "/" + this.questionEntered)
                    .success(function (response) {
                    self.questions.questions_array.push(self.questionEntered);
                    self.questions.questions_string = self.questions.questions_array.join('\n');
                    self.questionEntered = '';
                });
            }
        };
        LiveViewController.$inject = ["$scope", "$http", "$timeout"];
        return LiveViewController;
    }());
    ClassMoodApp.LiveViewController = LiveViewController;
    ClassMoodApp.app.controller('LiveViewController', LiveViewController);
})(ClassMoodApp || (ClassMoodApp = {}));
