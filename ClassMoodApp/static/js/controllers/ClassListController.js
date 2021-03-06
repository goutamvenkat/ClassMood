/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var ClassListController = (function () {
        function ClassListController($scope, $http, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$window = $window;
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            this.classes = [];
            this.getCurrentClasses();
            this.getIsProfessor();
            this.getUserId();
        }
        ClassListController.prototype.getCurrentClasses = function () {
            var _this = this;
            this.$http.get("/getClassList").success(function (data, status) {
                _this.classes = data.results;
            }).catch(function (error) {
                console.log(error);
            });
        };
        ClassListController.prototype.getUserId = function () {
            var _this = this;
            this.$http.get('/user_id').then(function (response) {
                _this.userId = response.data.results;
            });
        };
        ClassListController.prototype.getIsProfessor = function () {
            var _this = this;
            this.$http.get("/is_student").success(function (is_student, status) {
                _this.isStudent = is_student.results;
            });
        };
        ClassListController.prototype.addClass = function () {
            var _this = this;
            bootbox.prompt({
                title: "Enter Class Name",
                inputType: 'textarea',
                callback: function (className) {
                    if (className != null) {
                        if (_this.isStudent === true) {
                            _this.setStudentClass(className);
                        }
                        else {
                            _this.setProfClass(className);
                        }
                    }
                }
            });
        };
        ClassListController.prototype.setStudentClass = function (className) {
            var _this = this;
            this.$http.get("/set_student_classes/" + className + "/" + this.userId).then(function (response) {
                if (response.data === 'false') {
                    alert('Incorrect Class!');
                }
                else {
                    _this.getCurrentClasses();
                }
            });
        };
        ClassListController.prototype.setProfClass = function (className) {
            var _this = this;
            this.$http.get("/createClass/" + className).then(function (response) {
                if (response.data === 'false') {
                    alert('Incorrect Class!');
                }
                else {
                    _this.getCurrentClasses();
                }
            });
        };
        ClassListController.prototype.joinLecture = function (liveLectureId) {
            var _this = this;
            if (this.isStudent === true) {
                this.$http.get("/join_live_lecture/" + liveLectureId).then(function (response) {
                    console.log("JOINED LECTURE AND UPDATED STUDENT COUNT: " + response.data);
                    if (response.data !== undefined) {
                        var classId = parseInt(response.data, 10);
                        if (classId > 0) {
                            // At this point just open the lecture page so that students and professor are both viewing the same material (Except for gauges).
                            _this.$window.location.href = "/live_lecture/get/" + classId;
                        }
                        else {
                            alert("Invalid class id returned.");
                        }
                    }
                });
            }
        };
        ClassListController.prototype.deleteClass = function (classId) {
            var _this = this;
            if (this.isStudent) {
                this.$http.get("/delete/class_student/" + this.userId + "/" + classId).success(function (data, status) {
                    if (data.results === true) {
                        _this.getCurrentClasses();
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            }
            else {
                this.$http.get("/delete/class/" + classId).success(function (data, status) {
                    if (data.results === true) {
                        _this.getCurrentClasses();
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            }
        };
        ClassListController.prototype.getClassLectures = function (classId) {
            if (this.isStudent !== true) {
                this.$window.location.href = "/lectureList/" + classId;
            }
        };
        ClassListController.$inject = ["$scope", "$http", "$window"];
        return ClassListController;
    }());
    ClassMoodApp.ClassListController = ClassListController;
    ClassMoodApp.app.controller('ClassListController', ClassListController);
})(ClassMoodApp || (ClassMoodApp = {}));
