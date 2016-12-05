/// <reference path="../app.ts" />
/// <reference path="../../../../typings/bootbox/bootbox.d.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var LectureListController = (function () {
        function LectureListController($scope, $http, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$window = $window;
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            this.lectures = [];
        }
        LectureListController.prototype.init = function (classId) {
            this.classId = classId;
            this.getCurrentlectures();
            this.getIsProfessor();
            this.getUserId();
        };
        LectureListController.prototype.getCurrentlectures = function () {
            var _this = this;
            this.$http.get("/get_lecture_list/" + this.classId).success(function (data, status) {
                _this.lectures = data.results;
            }).catch(function (error) {
                console.log(error);
            });
        };
        LectureListController.prototype.getUserId = function () {
            var _this = this;
            this.$http.get('/user_id').then(function (response) {
                _this.userId = response.results;
            });
        };
        LectureListController.prototype.getIsProfessor = function () {
            var _this = this;
            this.$http.get("/is_student").success(function (is_student, status) {
                _this.isStudent = is_student.results;
            });
        };
        LectureListController.prototype.addLecture = function () {
            var _this = this;
            bootbox.prompt({
                title: "Enter Lecture Name",
                value: 'Lecture Name',
                callback: function (lectureName) {
                    if (lectureName != null) {
                        if (_this.isStudent !== true) {
                            _this.$http.get("/add_lecture/" + _this.classId + "/" + lectureName).then(function (response) {
                                console.log(response.data);
                            }).then(function () { _this.getCurrentlectures(); });
                        }
                    }
                }
            });
        };
        LectureListController.prototype.setStudentLecture = function (lectureName) {
            var _this = this;
            this.$http.get("/set_student_lectures/" + lectureName + "/" + this.userId).then(function (response) {
                if (response.data === 'false') {
                    alert('Incorrect Class!');
                }
                else {
                    _this.getCurrentlectures();
                }
            });
        };
        LectureListController.prototype.setProfLecture = function (lectureName) {
            var _this = this;
            this.$http.get("/createClass/" + lectureName).then(function (response) {
                if (response.data === 'false') {
                    alert('Incorrect Class!');
                }
                else {
                    _this.getCurrentlectures();
                }
            });
        };
        LectureListController.prototype.goLive = function (lectId) {
            var _this = this;
            this.$http.get("/live_lecture/create/" + lectId).then(function (response) {
                if (response.data !== undefined) {
                    var classId = parseInt(response.data, 10);
                    _this.$window.location.href = "/live_lecture/get/" + classId;
                }
            });
        };
        LectureListController.prototype.getPollingQuestions = function (lecture_id) {
            if (this.isStudent !== true) {
                this.$window.location.href = "/pollingQuestionList/" + this.classId + "/" + lecture_id;
            }
        };
        LectureListController.prototype.deleteLecture = function (lecture_id) {
            var _this = this;
            if (!this.isStudent) {
                this.$http.get("/delete/lecture/" + lecture_id).success(function (data, status) {
                    if (data.results === true) {
                        _this.getCurrentlectures();
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            }
        };
        LectureListController.$inject = ["$scope", "$http", "$window", "$routeParams"];
        return LectureListController;
    }());
    ClassMoodApp.LectureListController = LectureListController;
    ClassMoodApp.app.controller('LectureListController', LectureListController);
})(ClassMoodApp || (ClassMoodApp = {}));
