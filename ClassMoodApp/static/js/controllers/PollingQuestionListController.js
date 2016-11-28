/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var PollingQuestionListController = (function () {
        function PollingQuestionListController($scope, $http, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$window = $window;
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            var curLink = $window.location.pathname.split("/");
            this.classId = parseInt(curLink[curLink.length - 2]);
            this.lecture_id = parseInt(curLink[curLink.length - 1]);
            this.getPollingQuestions();
        }
        PollingQuestionListController.prototype.getPollingQuestions = function () {
            var _this = this;
            this.$http.get("/get_polling_questions/" + this.lecture_id).success(function (data, status) {
                _this.questions = data.results;
            }).catch(function (error) {
                console.log(error);
            });
        };
        PollingQuestionListController.prototype.goLive = function () {
            var _this = this;
            this.$http.get("/live_lecture/create/" + this.lecture_id).then(function (response) {
                var liveId = response.data;
                _this.$window.location.href = "/live_lecture/get/" + _this.classId;
            });
        };
        PollingQuestionListController.prototype.loadAddPollingQuestionsPage = function () {
            if (!this.isStudent) {
                this.$window.location.href = "/pollingQuestionList/" + this.classId + "/" + this.lecture_id + "/createPollingQuestion";
            }
        };
        PollingQuestionListController.prototype.deletePollingQuestion = function (id) {
            var _this = this;
            if (!this.isStudent) {
                this.$http.get("/delete/polling_question/" + id).success(function (data, status) {
                    if (data.results === true) {
                        _this.getPollingQuestions();
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            }
        };
        PollingQuestionListController.$inject = ["$scope", "$http", "$window"];
        return PollingQuestionListController;
    }());
    ClassMoodApp.PollingQuestionListController = PollingQuestionListController;
    ClassMoodApp.app.controller('PollingQuestionListController', PollingQuestionListController);
})(ClassMoodApp || (ClassMoodApp = {}));
