/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var ClassListController = (function () {
        function ClassListController($scope, $http) {
            this.$scope = $scope;
            this.$http = $http;
            this.$http = $http;
            this.$scope = $scope;
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
                        if (_this.isStudent) {
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
                if (response.data === false) {
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
                if (response.data === false) {
                    alert('Incorrect Class!');
                }
                else {
                    _this.getCurrentClasses();
                }
            });
        };
        ClassListController.prototype.addLecture = function () {
        };
        ClassListController.$inject = ["$scope", "$http"];
        return ClassListController;
    }());
    ClassMoodApp.ClassListController = ClassListController;
    ClassMoodApp.app.controller('ClassListController', ClassListController);
})(ClassMoodApp || (ClassMoodApp = {}));
